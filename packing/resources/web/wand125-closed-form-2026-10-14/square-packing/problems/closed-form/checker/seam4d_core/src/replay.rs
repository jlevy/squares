//! Mirrors the Python reference implementations of poly_lower and edge_check.
use super::*;
use serde_json::{json, Value};
pub type Box4 = [Q; 8];

/// edgefam.derive: preserve metadata and reload through the ordinary JSON loader.
pub fn derive_family_text(text: &str, kind: char) -> Result<String,String> {
    let mut d: Value = serde_json::from_str(text).map_err(|e|e.to_string())?;
    let a=json_q(d.get("UA").ok_or("missing UA")?)?;
    let keys: &[(&str,usize,usize)] = match kind {
        'X'=> &[("F",0,2)],
        'Y'=> &[("F",1,3),("T",1,3),("V",1,1)],
        _=>return Err("unknown edge variant".into()),
    };
    for &(key,i,j) in keys {
        let rows=d.get(key).and_then(Value::as_array).ok_or(format!("missing {key}"))?;
        let mut kept=vec![];
        for row in rows {
            let r=row.as_array().ok_or("segment is not an array")?;
            let x=json_q(r.get(i).ok_or("short segment")?)?;
            let y=json_q(r.get(j).ok_or("short segment")?)?;
            if !(x==a && y==a) { kept.push(row.clone()); }
        }
        d[key]=Value::Array(kept);
    }
    let a=a.to_string();
    d["U"]=if kind=='X' {json!([["-1000",a],["1000",a],["1000","1000"],["-1000","1000"]])}
        else {json!([[a,"-1000"],["1000","-1000"],["1000","1000"],[a,"1000"]])};
    d["edge_variant"]=json!(kind.to_string());
    serde_json::to_string(&d).map_err(|e|e.to_string())
}

/// Built once from the same input bytes as the original family; shared read-only.
pub struct EdgeVariants { pub x: FamilyCore, pub y: FamilyCore }
impl EdgeVariants {
    pub fn load(text: &str) -> Result<Self,String> {
        Ok(Self {x:load_family_text(&derive_family_text(text,'X')?)?,
                 y:load_family_text(&derive_family_text(text,'Y')?)?})
    }
}

pub fn poly_lower(f: &FamilyCore, b: &Box4) -> Q {
    let [x0,x1,y0,y1,u0,u1,_,_] = b;
    let lo = half(&wmin(u0,u1));
    let x0 = x0.max(&lo); let y0 = y0.max(&lo);
    if x0 > x1 || y0 > y1 { return qi(0); }
    let (cx,cy,rx,ry) = (half(&add(x0,x1)),half(&add(y0,y1)),half(&sub(x1,x0)),half(&sub(y1,y0)));
    let hp = angular_core_halfplanes(u0,u1).into_iter().map(|(a,b)| {
        let b = sub(&sub(&b,&mul(&absq(&a.0),&rx)),&mul(&absq(&a.1),&ry)); (a,b)
    }).collect::<Vec<_>>();
    let mut p = halfplanes_to_poly(&hp,&qi(2));
    for v in &mut p { v.0 += &cx; v.1 += &cy; }
    if p.len() >= 3 && area(&p) < 0 { p.reverse(); }
    let u = f.u_lower.clone();
    let inner = if p.len() >= 3 { clip_to(p,&u) } else { vec![] };
    let ai = if inner.len() >= 3 { area(&inner) } else { qi(0) };
    let o = outer_hull(u0,u1,&cx,&cy,&rx,&ry);
    let oc = clip_to(o.clone(),&u);
    let ao = sub(&qi(1),&sub(&area(&o),&if oc.len() >= 3 {area(&oc)} else {qi(0)}));
    ai.max(ao).max(qi(0))
}

type Piece = (Q,Q,Q);
fn pieces(raw: &[(Pt,Pt,Q)], a: &Q, vertical: bool) -> Result<Vec<Piece>,String> {
    let mut out = vec![];
    for (p,q,m) in raw {
        let (fixed0,fixed1,s,t) = if vertical {(&p.0,&q.0,&p.1,&q.1)} else {(&p.1,&q.1,&p.0,&q.0)};
        if fixed0 == a && fixed1 == a && *m > 0 {
            if s == t { return Err("positive zero-length EDGE segment".into()); }
            out.push((s.min(t).clone(),s.max(t).clone(),div(m,&absq(&sub(t,s)))));
        }
    }
    Ok(out)
}
fn sorted(mut v: Vec<Q>) -> Vec<Q> { v.sort(); v.dedup(); v }
fn density(p: &[Piece], x: &Q) -> Q {
    p.iter().filter(|(s,t,_)| s < x && x < t).fold(qi(0),|v,(_,_,r)| v+r)
}
// Python _sweep_min: group equal endpoints before inspecting each open span.
fn sweep_min(p: &[Piece], lo: &Q, hi: &Q) -> Q {
    let mut ev = vec![];
    for (s,t,r) in p {
        let a=s.max(lo); let b=t.min(hi);
        if a < b { ev.push((a.clone(),r.clone())); ev.push((b.clone(),neg(r))); }
    }
    ev.sort_by(|a,b| a.0.cmp(&b.0));
    let (mut cur,mut best,mut x,mut i) = (qi(0),None,lo.clone(),0);
    while i < ev.len() && ev[i].0 <= *lo { cur += &ev[i].1; i+=1; }
    loop {
        let nxt=if i<ev.len() { &ev[i].0 } else {hi};
        if *nxt > x { best=Some(best.map_or(cur.clone(),|v: Q| v.min(cur.clone()))); }
        if i>=ev.len() || nxt>=hi {break;}
        x=nxt.clone();
        while i<ev.len() && ev[i].0==x {cur+=&ev[i].1; i+=1;}
    }
    best.unwrap_or_else(||qi(0))
}
fn half_w_max(b: &Box4) -> Q {
    let m=absq(&b[4]).max(absq(&b[5]));
    if m<=qf(2,5) { let (c,s)=cs(&m); half(&add(&c,&s)) } else {qf(7072,10000)}
}
fn xline_min(f: &FamilyCore, lo: &Q, hi: &Q) -> Result<Q,String> {
    Ok(sweep_min(&pieces(&f.f_raw,&f.ua,true)?,lo,hi))
}
fn yline_min(f: &FamilyCore, lo: &Q, hi: &Q, e0: &Q, e1: &Q) -> Result<Q,String> {
    let a=&f.ua;
    let fp=pieces(&f.f_raw,a,false)?; let tp=pieces(&f.t_raw,a,false)?;
    let vp=f.v.iter().filter(|(_,y,r)| y==a && *r>qi(0)).collect::<Vec<_>>();
    let w=qi(crate::w0());      // Seam line x = w₀ + δ (default w₀ = 2).
    let mut cuts=vec![lo.clone(),hi.clone(),add(&w,e0),add(&w,e1)];
    for (s,t,_) in &fp { cuts.extend([s.clone(),t.clone()]); }
    for (xl,_,_) in &vp { cuts.push(xl.clone()); }
    for (s,t,_) in &tp { for p in [s,t] { for e in [e0,e1] {cuts.push(add(p,e));} } }
    let cuts=sorted(cuts.into_iter().filter(|c| lo<=c && c<=hi).collect());
    let mut best: Option<Q>=None;
    for pq in cuts.windows(2) {
        let x=half(&add(&pq[0],&pq[1]));
        let mut dc=vec![e0.clone(),e1.clone(),sub(&x,&w)];
        for (s,t,_) in &tp { dc.extend([sub(&x,s),sub(&x,t)]); }
        let dc=sorted(dc.into_iter().filter(|d| e0<=d && d<=e1).collect());
        for ds in dc.windows(2) {
            let d=half(&add(&ds[0],&ds[1]));
            let mut v=density(&fp,&x)+density(&tp,&sub(&x,&d));
            for (xl,_,rho) in &vp { if *xl<x && x<add(&w,&d) {v+=rho;} }
            best=Some(best.map_or(v.clone(),|m|m.min(v)));
        }
    }
    Ok(best.unwrap_or_else(||qi(0)))
}

/// check_record4d.side_check, including its short-circuit order.
pub fn side_check(f: &FamilyCore, b: &Box4, kind: char) -> Result<bool,String> {
    let w=half_w_max(b);
    let i=match kind {'X'=>0,'Y'=>2,_=>return Err("unknown edge variant".into())};
    if b[i]<f.ua {return Ok(false);}
    let h=add(&sub(&f.ua,&b[i]),&w);
    if h<=0 {return Ok(true);}
    let d=if kind=='X' {xline_min(f,&sub(&b[2],&w),&add(&b[3],&w))?}
        else {yline_min(f,&sub(&b[0],&w),&add(&b[1],&w),&b[6],&b[7])?};
    Ok(h<=d)
}
pub fn edge_values(f: &FamilyCore, b: &Box4) -> Result<Value,String> {
    let w=half_w_max(b);
    let hx=add(&sub(&f.ua,&b[0]),&w); let hy=add(&sub(&f.ua,&b[2]),&w);
    let dx=xline_min(f,&sub(&b[2],&w),&add(&b[3],&w))?;
    let dy=yline_min(f,&sub(&b[0],&w),&add(&b[1],&w),&b[6],&b[7])?;
    Ok(json!({"ok":side_check(f,b,'X')? && side_check(f,b,'Y')?,
        "hX":hx.to_string(),"hY":hy.to_string(),"densityX":dx.to_string(),"densityY":dy.to_string()}))
}

pub fn leaf_with_variants(f: &FamilyCore, variants: &EdgeVariants, b: &Box4, kind: &str) -> Value {
    let (k,base)=match kind {
        "EX:CORE"=>('X',"CORE"), "EX:B3D"=>('X',"B3D"),
        "EY:CORE"=>('Y',"CORE"), "EY:B3D"=>('Y',"B3D"),
        _=>return leaf(f,b,kind),
    };
    if (0..8).step_by(2).any(|i| b[i]>=b[i+1]) {return json!({"ok":false,"why":"nonpositive box interval"});}
    match side_check(f,b,k) {
        Ok(false)=>json!({"ok":false,"side":false,"why":format!("{kind} side condition fails")}),
        Err(e)=>json!({"ok":false,"why":e}),
        Ok(true)=>{
            let mut v=leaf(if k=='X' {&variants.x} else {&variants.y},b,base);
            v["side"]=json!(true); v
        }
    }
}
pub fn leaf(f: &FamilyCore,b: &Box4,kind: &str) -> Value {
    if (0..8).step_by(2).any(|i| b[i]>=b[i+1]) {return json!({"ok":false,"why":"nonpositive box interval"});}
    match kind {
        "EMPTY" => {let lo=half(&wmin(&b[4],&b[5])); json!({"ok":b[1]<lo || b[3]<lo,"lo":lo.to_string()})},
        "CORE" => {
            let [x0,x1,y0,y1,u0,u1,e0,e1]=b.clone();
            let v=f.bound_fast(x0,x1,y0,y1,u0,u1,e0,e1);
            json!({"ok":v.as_ref().is_some_and(|v|*v>=1),"bound":v.map(|v|v.to_string())})
        },
        "CORE1:x" | "CORE1:y" | "CORE1:xy" | "CORE1:xyh" |
        "CORE1:Tx" | "CORE1:Ty" | "CORE1:TxHy" | "CORE1:TyHx" | "CORE1:P" => {
            use b3d::Core1UTerm;
            if b[4]<0 && b[5]>0 { return json!({"ok":false,"why":format!("{kind} contains u=0")}); }
            let bx=[b[0].clone(),b[1].clone(),b[2].clone(),b[3].clone(),b[6].clone(),b[7].clone()];
            let mut p = None;
            let (term, thr) = match kind {
                "CORE1:P" => {
                    let lo = poly_lower(f,b);
                    let thr = sub(&qi(1), &lo); p = Some(lo);
                    (Core1UTerm::None, thr)
                },
                "CORE1:TxHy" | "CORE1:TyHx" => {
                    let (condition,k) = if kind=="CORE1:TxHy" {('X','x')} else {('Y','y')};
                    if !b3d::concave_ok(&bx,&b[4],&b[5],&(condition,f.ua.clone())) {
                        return json!({"ok":false,"why":format!("{kind} concave condition fails")});
                    }
                    (Core1UTerm::TanHalf(k),qi(2))
                },
                "CORE1:Tx" | "CORE1:Ty" => {
                    let k = if kind=="CORE1:Tx" {'x'} else {'y'};
                    if !b3d::tangent_ok(&bx,&b[4],&b[5],&(k,f.ua.clone())) {
                        return json!({"ok":false,"why":format!("{kind} tangent condition fails")});
                    }
                    let (cs,co) = if k=='x' {(half(&add(&bx[0],&bx[1])),bx[2].clone())}
                                  else {(half(&add(&bx[2],&bx[3])),bx[0].clone())};
                    (Core1UTerm::Tan(k,f.ua.clone(),cs,co),qi(1))
                },
                _ => {
                    let k = match kind {"CORE1:x"=>'x',"CORE1:y"=>'y',"CORE1:xy"=>'b',_=>'h'};
                    if !b3d::concave_ok(&bx,&b[4],&b[5],&(k,f.ua.clone())) {
                        return json!({"ok":false,"why":format!("{kind} concave condition fails")});
                    }
                    if k=='h' {(Core1UTerm::PolyH,qi(2))} else {(Core1UTerm::PolyU,qi(1))}
                },
            };
            let mut result = match f.certify_core1(&bx,&b[4],&b[5],&thr,&qi(1),term) {
                Ok(r) => {
                    let d = if r.ok {json!({"ok":true,"values":r.values})}
                            else {json!({"ok":false,"why":r.why,"at":r.at})};
                    json!({"ok":r.ok,"certify_core1":d})
                },
                Err(e) => json!({"ok":false,"why":format!("CORE1 error: {e:?}")}),
            };
            if let Some(p) = p { result["P_lo"] = json!(p.to_string()); }
            result
        },
        "B4U" => {
            if b[4]<0 && b[5]>0 {return json!({"ok":false,"why":"B4U contains u=0"});}
            let bx=[b[0].clone(),b[1].clone(),b[2].clone(),b[3].clone(),b[6].clone(),b[7].clone()];
            match f.certify_b4u(&bx,&b[4],&b[5],&qi(1)) {
                Ok(r)=> {
                    let d=if r.ok {json!({"ok":true,"planes":r.planes,"dropped":r.dropped,
                        "triples":r.triples,"values":r.values,"edge_runs":r.edge_runs})}
                    else {json!({"ok":false,"why":r.why,"triple":r.triple,"at":r.at})};
                    json!({"ok":r.ok,"certify3":d})
                },
                Err(e)=>json!({"ok":false,"why":format!("B4U error: {e:?}")}),
            }
        },
        "B3D" => {
            if b[4]<0 && b[5]>0 { return json!({"ok":false,"why":"B3D contains u=0"}); }
            let p=poly_lower(f,b); let thr=sub(&qi(1),&p);
            let bx=[b[0].clone(),b[1].clone(),b[2].clone(),b[3].clone(),b[6].clone(),b[7].clone()];
            match f.certify3(&bx,&b[4],&b[5],&thr,&qi(1),None,None) {
                Ok(r)=>{
                    let d=if r.ok { json!({"ok":true,"planes":r.planes,"dropped":r.dropped,"triples":r.triples,"values":r.values}) }
                    else {json!({"ok":false,"why":r.why,"triple":r.triple,"at":r.at})};
                    json!({"ok":r.ok,"P_lo":p.to_string(),"certify3":d})
                },
                Err(e)=>json!({"ok":false,"P_lo":p.to_string(),"why":format!("B3D error: {e:?}")})
            }
        },
        "B3U:x" | "B3U:y" | "B3U:xy" | "B3U:xyh" => {
            if b[4]<0 && b[5]>0 { return json!({"ok":false,"why":format!("{kind} contains u=0")}); }
            let bx=[b[0].clone(),b[1].clone(),b[2].clone(),b[3].clone(),b[6].clone(),b[7].clone()];
            let c=(match kind {"B3U:x"=>'x', "B3U:y"=>'y', "B3U:xy"=>'b', _=>'h'},f.ua.clone());
            let thr_u = if kind=="B3U:xyh" {qi(2)} else {qi(1)};
            if !b3d::concave_ok(&bx,&b[4],&b[5],&c) {
                return json!({"ok":false,"why":format!("{kind} concave condition fails")});
            }
            match f.certify3(&bx,&b[4],&b[5],&thr_u,&qi(1),Some(c),None) {
                Ok(r)=>{
                    let mut d=json!({"ok":r.ok});
                    if r.ok { d=json!({"ok":true,"planes":r.planes,"dropped":r.dropped,"triples":r.triples,"values":r.values}); }
                    else { d["why"]=json!(r.why); if let Some(t)=r.triple { d["triple"]=json!(t); } if let Some(at)=r.at { d["at"]=json!(at); } }
                    json!({"ok":r.ok,"certify3":d})
                },
                Err(e)=>json!({"ok":false,"why":format!("B3U error: {e:?}")})
            }
        },
        "B3T:x" | "B3T:y" => {
            if b[4]<0 && b[5]>0 { return json!({"ok":false,"why":format!("{kind} contains u=0")}); }
            let bx=[b[0].clone(),b[1].clone(),b[2].clone(),b[3].clone(),b[6].clone(),b[7].clone()];
            let c=(if kind=="B3T:x" {'x'} else {'y'},f.ua.clone());
            if !b3d::tangent_ok(&bx,&b[4],&b[5],&c) {
                return json!({"ok":false,"why":format!("{kind} tangent condition fails")});
            }
            match f.certify3(&bx,&b[4],&b[5],&qi(1),&qi(1),None,Some(c)) {
                Ok(r)=>{
                    let mut d=json!({"ok":r.ok});
                    if r.ok { d=json!({"ok":true,"planes":r.planes,"dropped":r.dropped,"triples":r.triples,"values":r.values}); }
                    else { d["why"]=json!(r.why); if let Some(t)=r.triple { d["triple"]=json!(t); } if let Some(at)=r.at { d["at"]=json!(at); } }
                    json!({"ok":r.ok,"certify3":d})
                },
                Err(e)=>json!({"ok":false,"why":format!("B3T error: {e:?}")})
            }
        },
        "EDGE"=>edge_values(f,b).unwrap_or_else(|e|json!({"ok":false,"why":e})),
        _=>json!({"ok":false,"why":format!("unsupported kind {kind}")})
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    const FAMILY: &str = r#"{"d0":"0","d1":"1/10","UA":"1","U":[["7","7"],["8","7"],["8","8"]],"F":[["1","0","1","4","8"],["0","1","4","1","8"],["1","2","1","3","0"]],"T":[["0","1","4","1","4"],["0","2","4","2","4"]],"V":[["0","1","2"],["0","2","3"]]}"#;
    #[test]
    fn b4u_leaf_routing_and_preconditions() {
        let f=load_family_text(r#"{"d0":0,"d1":1,"UA":1,"F":[],"T":[],"V":[]}"#).unwrap();
        let mut b=["2","3","2","3","0","1/10","0","1"].map(|s|parse_fraction(s).unwrap());
        for (a,z) in [(qi(0),qf(1,10)),(qf(-1,10),qi(0))] {
            b[4]=a; b[5]=z;
            let r=leaf(&f,&b,"B4U"); assert_eq!(r["ok"],true,"{r}");
            assert!(r["certify3"]["edge_runs"].as_u64().unwrap()>0);
        }
        b[5]=qf(1,10);
        assert_eq!(leaf(&f,&b,"B4U")["why"],"B4U contains u=0");
        b[4]=qi(0); b[0]=qf(1,10); b[1]=qf(1,5);
        assert_eq!(leaf(&f,&b,"B4U")["ok"],false); // no local U
        b[0]=qf(4,5); b[1]=qf(9,10);
        assert_eq!(leaf(&f,&b,"B4U")["certify3"]["why"],"value");
        b[1]=b[0].clone();
        assert_eq!(leaf(&f,&b,"B4U")["why"],"nonpositive box interval");
    }

    #[test]
    fn core1_leaf_routing_and_conditions() {
        let f=load_family_text(r#"{"d0":0,"d1":1,"UA":1,"F":[],"T":[],"V":[]}"#).unwrap();
        let mut b=["2","3","2","3","0","1/10","0","1"].map(|s|parse_fraction(s).unwrap());
        let kinds=["CORE1:x","CORE1:y","CORE1:xy","CORE1:xyh","CORE1:Tx","CORE1:Ty","CORE1:P"];
        for k in ["CORE1:x","CORE1:y","CORE1:xy","CORE1:xyh","CORE1:P"] {
            let r=leaf(&f,&b,k); assert_eq!(r["ok"],true,"{k}: {r}");
            assert!(r["certify_core1"]["values"].as_u64().unwrap()>=8);
        }
        for k in ["CORE1:Tx","CORE1:Ty"] {
            assert_eq!(leaf(&f,&b,k)["why"],format!("{k} tangent condition fails"));
        }
        b[4]=qf(-1,10);
        for k in kinds { assert_eq!(leaf(&f,&b,k)["why"],format!("{k} contains u=0")); }
        b[4]=qi(0); b[0]=qf(1,10); b[1]=qf(1,5);
        for k in ["CORE1:x","CORE1:y","CORE1:xy","CORE1:xyh"] {
            assert_eq!(leaf(&f,&b,k)["why"],format!("{k} concave condition fails"));
        }
        assert_eq!(leaf(&f,&b,"CORE1:Tx")["certify_core1"]["why"],"core1-domain");
        assert_eq!(leaf(&f,&b,"CORE1:P")["certify_core1"]["why"],"core1-domain");
        b[0]=qf(4,5); b[1]=qf(9,10);
        assert_eq!(leaf(&f,&b,"CORE1:Tx")["certify_core1"]["why"],"value");
        b.swap(0,2); b.swap(1,3);
        assert_eq!(leaf(&f,&b,"CORE1:Ty")["certify_core1"]["why"],"value");
    }

    #[test]
    fn core1_tan_half_leaf_conditions_and_threshold() {
        let f=load_family_text(r#"{"d0":0,"d1":1,"UA":1,"F":[],"T":[],"V":[]}"#).unwrap();
        for k in ["CORE1:TxHy","CORE1:TyHx"] {
            let mut b=["4/5","9/10","2","3","0","1/10","0","1"].map(|s|parse_fraction(s).unwrap());
            if k=="CORE1:TyHx" { b.swap(0,2); b.swap(1,3); }
            // Sum exceeds 1 but is below 2: catches an incorrect threshold of 1.
            assert_eq!(leaf(&f,&b,k)["certify_core1"]["why"],"value");
            b[4]=qf(-1,10);
            assert_eq!(leaf(&f,&b,k)["why"],format!("{k} contains u=0"));
            b[4]=qi(0);
            let outer = if k=="CORE1:TxHy" {0} else {2};
            b[outer]=qf(1,10); b[outer+1]=qf(1,5);
            assert_eq!(leaf(&f,&b,k)["certify_core1"]["why"],"core1-domain");
            b[outer]=qi(2); b[outer+1]=qi(3);
            assert_eq!(leaf(&f,&b,k)["why"],format!("{k} concave condition fails"));
        }
    }

    #[test]
    fn b3t_rejects_zero_and_bad_tangent() {
        let f=load_family_text(FAMILY).unwrap();
        let mut b=["0","1/10","2","21/10","-1/100","1/100","0","1/10"].map(|s|parse_fraction(s).unwrap());
        for k in ["B3T:x","B3T:y"] {
            assert_eq!(leaf(&f,&b,k)["why"],format!("{k} contains u=0"));
        }
        b[4]=qi(0); b[1]=qi(2);
        for k in ["B3T:x","B3T:y"] {
            assert_eq!(leaf(&f,&b,k)["why"],format!("{k} tangent condition fails"));
        }
        b[0]=qi(2);
        assert_eq!(leaf(&f,&b,"B3T:x")["why"],"nonpositive box interval");
    }

    #[test]
    fn b3u_rejects_zero_and_bad_concavity() {
        let f=load_family_text(FAMILY).unwrap();
        let mut b=["1","11/10","2","21/10","-1/100","1/100","0","1/10"].map(|s|parse_fraction(s).unwrap());
        for k in ["B3U:x","B3U:y"] {
            assert_eq!(leaf(&f,&b,k)["why"],format!("{k} contains u=0"));
        }
        b[4]=qi(0); b[0]=qf(999,1000);
        for k in ["B3U:x","B3U:y"] {
            assert_eq!(leaf(&f,&b,k)["why"],format!("{k} concave condition fails"));
        }
    }
    #[test]
    fn derive_removes_all_line_segments_and_replaces_u() {
        let x:Value=serde_json::from_str(&derive_family_text(FAMILY,'X').unwrap()).unwrap();
        let y:Value=serde_json::from_str(&derive_family_text(FAMILY,'Y').unwrap()).unwrap();
        assert_eq!(x["F"].as_array().unwrap().len(),1); // Includes removal of zero mass.
        assert_eq!(x["T"].as_array().unwrap().len(),2);
        for key in ["F","T","V"] {assert_eq!(y[key].as_array().unwrap().len(),if key=="F" {2} else {1});}
        let vs=EdgeVariants::load(FAMILY).unwrap();
        assert_eq!(vs.x.u,vs.x.u_lower); assert_eq!(vs.y.u,vs.y.u_lower);
        assert_eq!(vs.x.u[0],(qi(-1000),qi(1)));
        assert_eq!(vs.y.u[0],(qi(1),qi(-1000)));
        assert_eq!(vs.x.d1,qf(1,10)); assert_eq!(vs.y.ua,qi(1));
    }
    #[test]
    fn side_uses_original_family_and_rejects_below_ua() {
        let f=load_family_text(FAMILY).unwrap(); let vs=EdgeVariants::load(FAMILY).unwrap();
        let mut b=["1","11/10","1","11/10","0","1/100","0","1/10"].map(|s|parse_fraction(s).unwrap());
        for k in ['X','Y'] {
            assert!(side_check(&f,&b,k).unwrap());
            assert!(!side_check(if k=='X' {&vs.x} else {&vs.y},&b,k).unwrap());
            assert_eq!(leaf_with_variants(&f,&vs,&b,&format!("E{k}:CORE"))["side"],true);
        }
        assert_eq!(edge_values(&f,&b).unwrap()["ok"],true);
        b[0]=qf(999,1000);
        assert_eq!(leaf_with_variants(&f,&vs,&b,"EX:B3D")["side"],false);
        b[0]=qi(1); b[2]=qf(999,1000);
        assert_eq!(leaf_with_variants(&f,&vs,&b,"EY:CORE")["side"],false);
    }
    #[test]
    fn variant_b3d_rejects_cross_zero_and_core_none() {
        let f=load_family_text(FAMILY).unwrap(); let vs=EdgeVariants::load(FAMILY).unwrap();
        let b=["1","11/10","1","11/10","-1/100","1/100","0","1/10"].map(|s|parse_fraction(s).unwrap());
        for k in ["EX:B3D","EY:B3D"] {assert_eq!(leaf_with_variants(&f,&vs,&b,k)["why"],"B3D contains u=0");}
        let text=r#"{"UA":"0","d0":"0","d1":"1","F":[["0","-2","0","2","8"],["-2","0","2","0","8"]],"T":[],"V":[]}"#;
        let f=load_family_text(text).unwrap();let vs=EdgeVariants::load(text).unwrap();
        let b=["0","1/10","0","1/10","0","1/100","0","1"].map(|s|parse_fraction(s).unwrap());
        for k in ["EX:CORE","EY:CORE"] {
            let r=leaf_with_variants(&f,&vs,&b,k);
            assert_eq!(r["side"],true);assert_eq!(r["ok"],false);assert!(r["bound"].is_null());
        }
    }
}
