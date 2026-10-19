use seam4d_core::{parse_fraction,Q,FamilyCore};
use seam4d_core::replay::{Box4,leaf_with_variants,EdgeVariants};
use serde_json::{json,Value};
use std::collections::{BTreeMap,BTreeSet};
use std::sync::{Mutex,atomic::{AtomicUsize,Ordering}};
mod sha256;

#[derive(Clone)] struct Leaf { b: Box4, kind: String }
struct Root { b: Box4, leaves: Vec<Leaf>, uncert: bool, source: String }
fn parse_box(v: &Value)->Result<Box4,String> {
    let a=v.as_array().ok_or("box is not an array")?;
    if a.len()!=8 {return Err("box must have 8 rational strings".into());}
    let b: Vec<Q>=a.iter().map(|x|parse_fraction(x.as_str().ok_or("box coordinate is not a string")?)).collect::<Result<_,String>>()?;
    let b: Box4=b.try_into().unwrap();
    if (0..8).step_by(2).any(|i|b[i]>=b[i+1]) {return Err("box has nonpositive interval".into());}
    Ok(b)
}
fn parse_leaf(v:&Value)->Result<Leaf,String> {
    let a=v.as_array().ok_or("leaf is not an array")?;
    if a.len()!=2 {return Err("leaf must be [box,kind]".into());}
    Ok(Leaf {b:parse_box(&a[0])?,kind:a[1].as_str().ok_or("kind is not a string")?.into()})
}
fn strings(b:&Box4)->Vec<String> {b.iter().map(ToString::to_string).collect()}
fn tiles(b:&Box4,leaves:&[Leaf])->bool {
    let mut stack=vec![(b.clone(),(0..leaves.len()).collect::<Vec<_>>())];
    while let Some((b,l))=stack.pop() {
        if l.len()==1 && leaves[l[0]].b==b {continue;}
        if l.is_empty() {return false;}
        let mut done=false;
        for k in [4,6,0,2] {
            let m=Q::from(&b[k]+&b[k+1])/2u32;
            let lo=l.iter().copied().filter(|&i|leaves[i].b[k+1]<=m).collect::<Vec<_>>();
            let hi=l.iter().copied().filter(|&i|leaves[i].b[k]>=m).collect::<Vec<_>>();
            if lo.len()+hi.len()==l.len() && !lo.is_empty() && !hi.is_empty() {
                let mut b1=b.clone(); b1[k+1]=m.clone();let mut b2=b.clone();b2[k]=m;
                stack.push((b1,lo));stack.push((b2,hi));done=true;break;
            }
        }
        if !done {return false;}
    }
    true
}
fn partition(ivs:&BTreeSet<(Q,Q)>,lo:&Q,hi:&Q)->bool {
    let v=ivs.iter().collect::<Vec<_>>();
    !v.is_empty() && &v[0].0==lo && &v[v.len()-1].1==hi && v.iter().all(|p|p.0<p.1) && v.windows(2).all(|p|p[0].1==p[1].0)
}
fn domain(roots:&[Root],reg:&[Q;4],f:&FamilyCore)->Vec<Value> {
    let mut bad=vec![];
    let mut fail=|s:&str|bad.push(json!({"source":"domain","why":s}));
    if roots.is_empty() {fail("no roots");return bad;}
    let axes=(0..8).step_by(2).map(|k|roots.iter().map(|r|(r.b[k].clone(),r.b[k+1].clone())).collect::<BTreeSet<_>>()).collect::<Vec<_>>();
    let u0=&axes[2].first().unwrap().0; let u1=axes[2].iter().map(|p| &p.1).max().unwrap();
    let a=Q::from(-u0);let sum=Q::from(&a+u1)+Q::from(&a*u1);
    if !(u0<&Q::from(0) && u1>&Q::from(0) && a<1 && *u1<1 && sum>=1) {fail("u-range does not cover 90 degrees");}
    if !(partition(&axes[0],&reg[0],&reg[1]) && partition(&axes[1],&reg[2],&reg[3]) && partition(&axes[2],u0,u1) && partition(&axes[3],&f.d0,&f.d1)) {fail("root intervals are not partitions");}
    let unique=roots.iter().map(|r|&r.b).collect::<BTreeSet<_>>();
    // Each root belongs to the product by construction. Equal cardinalities imply equality,
    // avoiding materializing a potentially huge product from a damaged record.
    let product=axes.iter().try_fold(1usize,|n,v|n.checked_mul(v.len()));
    if product!=Some(unique.len()) || unique.len()!=roots.len() {fail("roots are not exactly the product grid");}
    if roots.iter().any(|r|r.b[4]<0 && r.b[5]>0) {fail("a root contains u = 0 inside");}
    bad
}
fn source_hash()->String {
    let files: &[(&str,&[u8])]=&[
        ("Cargo.toml",include_bytes!("../Cargo.toml")),
        ("../Cargo.toml",include_bytes!("../../Cargo.toml")),
        ("../Cargo.lock",include_bytes!("../../Cargo.lock")),
        ("src/main.rs",include_bytes!("main.rs")),("src/sha256.rs",include_bytes!("sha256.rs")),
        ("../seam4d_core/Cargo.toml",include_bytes!("../../seam4d_core/Cargo.toml")),
        ("../seam4d_core/src/lib.rs",include_bytes!("../../seam4d_core/src/lib.rs")),
        ("../seam4d_core/src/fast.rs",include_bytes!("../../seam4d_core/src/fast.rs")),
        ("../seam4d_core/src/b3d.rs",include_bytes!("../../seam4d_core/src/b3d.rs")),
        ("../seam4d_core/src/replay.rs",include_bytes!("../../seam4d_core/src/replay.rs"))];
    let mut bytes=vec![];
    for (name,data) in files {bytes.extend(name.as_bytes());bytes.push(0);bytes.extend((data.len() as u64).to_be_bytes());bytes.extend(*data);}
    sha256::digest(&bytes)
}
// POSIX clock(): process CPU time, including worker threads; Linux/macOS CLOCKS_PER_SEC=1e6.
fn cpu()->f64 {unsafe extern "C" {fn clock()->std::os::raw::c_long;} unsafe {clock() as f64/1_000_000.0}}
fn run()->Result<bool,String> {
    let start=std::time::Instant::now();let cpu0=cpu();
    let args=std::env::args().skip(1).collect::<Vec<_>>();
    let (mut paths,mut reg,mut out,mut threads,mut leaves_mode)=(vec![],None,None,1usize,false);
    let mut i=0;
    while i<args.len() {
        match args[i].as_str() {
            "--region"=>{if i+4>=args.len(){return Err("--region needs four values".into());} let v=args[i+1..i+5].iter().map(|s|parse_fraction(s)).collect::<Result<Vec<_>,_>>()?;reg=Some(<[Q;4]>::try_from(v).unwrap());i+=4;},
            "--threads"=>{i+=1;threads=args.get(i).ok_or("missing threads")?.parse().map_err(|_|"invalid threads")?;if threads==0{return Err("threads must be positive".into());}},
            "--out"=>{i+=1;out=Some(args.get(i).ok_or("missing out path")?.clone());},
            "--leaves"=>leaves_mode=true,
            s if s.starts_with("--")=>return Err(format!("unknown option {s}")),
            s=>paths.push(s.to_string())
        } i+=1;
    }
    if paths.len()<2 || (!leaves_mode && reg.is_none()) {return Err("usage: replay4d family.json record.jsonl [...] --region X0 X1 Y0 Y1 [--threads N] [--out summary.json]; --leaves uses JSONL [box,kind] lines without domain/tiling checks".into());}
    if out.as_ref().is_some_and(|o|paths.iter().any(|p|std::path::Path::new(p).canonicalize().ok()==std::path::Path::new(o).canonicalize().ok() && std::path::Path::new(o).exists())) {return Err("--out must not overwrite an input".into());}
    let family_bytes=std::fs::read(&paths[0]).map_err(|e|e.to_string())?;
    // Parse the same bytes that are hashed (no second read of a possibly changing family).
    let f=seam4d_core::load_family_text(std::str::from_utf8(&family_bytes).map_err(|e|e.to_string())?)?;
    let variants=EdgeVariants::load(std::str::from_utf8(&family_bytes).map_err(|e|e.to_string())?)?;
    let mut hashes=vec![];let mut roots=vec![];let mut bad=vec![];
    for path in &paths[1..] {
        let bytes=std::fs::read(path).map_err(|e|e.to_string())?;
        hashes.push(json!({"path":path,"sha256":sha256::digest(&bytes)}));
        let text=std::str::from_utf8(&bytes).map_err(|e|e.to_string())?;
        for (n,line) in text.lines().enumerate() {
            let src=format!("{path}:{}",n+1);
            let parsed=(||->Result<Option<Root>,String>{
                let r:Value=serde_json::from_str(line).map_err(|e|e.to_string())?;
                if r.get("header").is_some(){return Ok(None);}
                if leaves_mode {let l=parse_leaf(&r)?;return Ok(Some(Root{b:l.b.clone(),leaves:vec![l],uncert:false,source:src.clone()}));}
                let b=parse_box(&r["root"])?;
                let uncert=!r["uncert"].as_array().ok_or("missing uncert array")?.is_empty();
                let leaves=r["leaves"].as_array().ok_or("missing leaves array")?.iter().map(parse_leaf).collect::<Result<Vec<_>,_>>()?;
                Ok(Some(Root{b,leaves,uncert,source:src.clone()}))
            })();
            match parsed {Ok(Some(r))=>roots.push(r),Ok(None)=>{},Err(e)=>bad.push(json!({"source":src,"why":e}))}
        }
    }
    if !leaves_mode {bad.extend(domain(&roots,&reg.unwrap(),&f));} else if roots.is_empty() {bad.push(json!({"why":"no leaves"}));}
    let mut kinds=BTreeMap::<String,usize>::new();for r in &roots {for l in &r.leaves {*kinds.entry(l.kind.clone()).or_default()+=1;}}
    let next=AtomicUsize::new(0);let results=Mutex::new(Vec::<(usize,Vec<Value>,Vec<Value>)>::new());
    #[cfg(feature = "prof")]
    let profiles = Mutex::new(Vec::new());
    std::thread::scope(|scope| {
        for _ in 0..threads.min(roots.len().max(1)) {
            let (roots,f,variants,next,results)=(&roots,&f,&variants,&next,&results);
            #[cfg(feature = "prof")]
            let profiles = &profiles;
            scope.spawn(move || { loop {
                let i=next.fetch_add(1,Ordering::Relaxed);if i>=roots.len(){break;}
                let r=&roots[i];let mut errors=vec![];let mut values=vec![];
                if r.uncert {errors.push(json!({"source":r.source,"why":"uncert"}));}
                if !leaves_mode && !tiles(&r.b,&r.leaves) {errors.push(json!({"source":r.source,"why":"leaves do not tile the root"}));}
                for (j,l) in r.leaves.iter().enumerate() {
                    let v=std::panic::catch_unwind(std::panic::AssertUnwindSafe(||leaf_with_variants(f,variants,&l.b,&l.kind))).unwrap_or_else(|_|json!({"ok":false,"why":"calculation panicked"}));
                    if v["ok"]!=true {errors.push(json!({"source":r.source,"leaf":j,"box":strings(&l.b),"kind":l.kind,"result":v}));}
                    if leaves_mode {values.push(json!({"source":r.source,"box":strings(&l.b),"kind":l.kind,"result":v}));}
                }
                results.lock().unwrap().push((i,errors,values));
            }
            #[cfg(feature = "prof")]
            profiles.lock().unwrap().extend(seam4d_core::b3d::prof::dump());
            });
        }
    });
    #[cfg(feature = "prof")]
    {
        let mut totals = BTreeMap::<String, (u64, f64)>::new();
        for (name, calls, seconds) in profiles.into_inner().unwrap() {
            let t = totals.entry(name).or_default(); t.0 += calls; t.1 += seconds;
        }
        let mut rows = totals.into_iter().collect::<Vec<_>>();
        rows.sort_by(|a,b| b.1.1.total_cmp(&a.1.1));
        for (name, (calls, seconds)) in rows { eprintln!("PROF {name} {calls} {seconds:.6}"); }
    }
    let mut results=results.into_inner().unwrap();results.sort_by_key(|r|r.0);
    let mut values=vec![];for (_,errs,vals) in results {bad.extend(errs);values.extend(vals);}
    let cpu_seconds=cpu()-cpu0;let wall_seconds=start.elapsed().as_secs_f64();
    let ok=bad.is_empty();
    let summary=json!({"mode":if leaves_mode{"leaves"}else{"replay"},"ok":ok,"roots":if leaves_mode{0}else{roots.len()},"kinds":kinds,
        "bad_count":bad.len(),"bad":bad.iter().take(20).collect::<Vec<_>>(),"cpu_seconds":cpu_seconds,"wall_seconds":wall_seconds,
        "family":{"path":paths[0],"sha256":sha256::digest(&family_bytes)},"records":hashes,"version":env!("CARGO_PKG_VERSION"),"source_sha256":source_hash(),"leaves":values});
    println!("roots {} leaf kinds {}",summary["roots"],summary["kinds"]);
    for e in bad.iter().take(20){println!("BAD {e}");}
    if leaves_mode {for v in summary["leaves"].as_array().unwrap(){println!("LEAF {v}");}}
    println!("cpu {cpu_seconds:.6}s wall {wall_seconds:.6}s");
    if let Some(path)=out {std::fs::write(path,serde_json::to_vec_pretty(&summary).unwrap()).map_err(|e|e.to_string())?;}
    if ok {println!("REPLAY OK");} else {println!("REPLAY BAD ({})",bad.len());}
    Ok(ok)
}
fn main() {match run() {Ok(true)=>{},Ok(false)=>std::process::exit(1),Err(e)=>{eprintln!("BAD {e}");println!("REPLAY BAD (1)");std::process::exit(2);}}}

#[cfg(test)]
mod tests {
    use super::*;
    fn b(v: [&str;8])->Box4 {v.map(|s|parse_fraction(s).unwrap())}
    #[test]
    fn tiling_and_damage() {
        let root=b(["0","1","0","1","-1/2","0","0","1"]);
        let mut lo=root.clone();lo[5]=Q::from((-1,4));
        let mut hi=root.clone();hi[4]=Q::from((-1,4));
        let mut leaves=vec![Leaf{b:lo,kind:"CORE".into()},Leaf{b:hi,kind:"CORE".into()}];
        assert!(tiles(&root,&leaves));
        assert!(!tiles(&root,&leaves[..1]));
        leaves.push(leaves[0].clone());assert!(!tiles(&root,&leaves));leaves.pop();
        leaves[0].b[0]+=Q::from((1,1000000));assert!(!tiles(&root,&leaves));
    }
    #[test]
    fn rational_parser_and_rejection() {
        assert_eq!(parse_fraction("9007199254740993/9007199254740992").unwrap()-1,Q::from((1i64,9007199254740992i64)));
        assert!(parse_fraction("1/0").is_err());
        assert!(parse_box(&json!(["0","0","0","1","0","1","0","1"])).is_err());
        assert!(parse_box(&json!([0,"1","0","1","0","1","0","1"])).is_err());
    }
    #[test]
    fn domain_uses_maximum_upper_endpoint() {
        let f=seam4d_core::load_family_text(r#"{"d0":"0","d1":"1","UA":"9/5","F":[],"T":[],"V":[]}"#).unwrap();
        let roots=[b(["0","1","0","1","-1/2","1/2","0","1"]),b(["0","1","0","1","1/10","1/5","0","1"])].map(|b|Root {b,leaves:vec![],uncert:false,source:"test".into()});
        let bad=domain(&roots,&[Q::from(0),Q::from(1),Q::from(0),Q::from(1)],&f);
        assert!(bad.iter().any(|v|v["why"]=="root intervals are not partitions"));
        assert!(!bad.iter().any(|v|v["why"]=="u-range does not cover 90 degrees"));
    }

}
