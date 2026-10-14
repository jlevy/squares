//! Fallible CPython 3.12 powersort comparison order for symbolic RF keys.
//! Comparing extra/different pairs can change the recorded guard trace.
//! Algorithm adapted from CPython 3.12 Objects/listobject.c (PSF license;
//! see CPYTHON_SORT_LICENSE). Payload moves do not invoke the comparator.

pub(super) fn sort<T: Clone, E>(a: &mut [T], mut lt: impl FnMut(&T, &T) -> Result<bool, E>) -> Result<(), E> {
    let total=a.len();
    let mut minrun=total; let mut rem=0;
    while minrun>=64 {rem|=minrun&1;minrun>>=1;}
    minrun+=rem;
    let mut stack: Vec<(usize,usize,usize)>=Vec::new();
    let mut min_gallop=7; let mut base=0;
    while base<total {
        let mut n=1;
        if base+1<total {
            let descending=lt(&a[base+1],&a[base])?;
            n=2;
            while base+n<total {
                if lt(&a[base+n],&a[base+n-1])?!=descending {break;}
                n+=1;
            }
            if descending {a[base..base+n].reverse();}
        }
        if n<minrun {
            let force=minrun.min(total-base);
            for start in base+n..base+force {
                let mut l=base;let mut r=start;
                while l<r {
                    let m=l+(r-l)/2;
                    if lt(&a[start],&a[m])? {r=m;} else {l=m+1;}
                }
                a[l..=start].rotate_right(1);
            }
            n=force;
        }
        if let Some(&(s1,n1,_))=stack.last() {
            let power=power(s1,n1,n,total);
            while stack.len()>1 && stack[stack.len()-2].2>power {
                let i=stack.len()-2;
                merge_at(a,&mut stack,i,&mut min_gallop,&mut lt)?;
            }
            stack.last_mut().unwrap().2=power;
        }
        stack.push((base,n,0));base+=n;
    }
    while stack.len()>1 {
        let mut i=stack.len()-2;
        if i>0 && stack[i-1].1<stack[i+1].1 {i-=1;}
        merge_at(a,&mut stack,i,&mut min_gallop,&mut lt)?;
    }
    Ok(())
}
fn power(s:usize,n1:usize,n2:usize,n:usize)->usize {
    let mut a=2*s+n1;let mut b=a+n1+n2;let mut p=0;
    loop {
        p+=1;
        if a>=n {a-=n;b-=n;} else if b>=n {return p;}
        a*=2;b*=2;
    }
}
// right=false: first >= key; right=true: first > key. Keep comparator
// operand order and exponential-search probes identical to Python.
fn gallop<T,E,F: FnMut(&T,&T)->Result<bool,E>>(key:&T,a:&[T],hint:usize,right:bool,lt:&mut F)->Result<usize,E> {
    let before=|x:&T,lt:&mut F| -> Result<bool,E> {
        if right {lt(key,x).map(|v|!v)} else {lt(x,key)}
    };
    let mut last=0isize;let mut ofs=1isize;let h=hint as isize;
    if before(&a[hint],lt)? {
        let max=(a.len()-hint) as isize;
        while ofs<max {
            if !before(&a[(h+ofs) as usize],lt)? {break;}
            last=ofs;ofs=ofs*2+1;
        }
        ofs=ofs.min(max);last+=h;ofs+=h;
    } else {
        let max=h+1;
        while ofs<max {
            if before(&a[(h-ofs) as usize],lt)? {break;}
            last=ofs;ofs=ofs*2+1;
        }
        ofs=ofs.min(max);let old=last;last=h-ofs;ofs=h-old;
    }
    last+=1;
    while last<ofs {
        let m=last+(ofs-last)/2;
        if before(&a[m as usize],lt)? {last=m+1;} else {ofs=m;}
    }
    Ok(ofs as usize)
}
fn merge_at<T:Clone,E>(a:&mut [T],stack:&mut Vec<(usize,usize,usize)>,i:usize,mg:&mut usize,
                       lt:&mut impl FnMut(&T,&T)->Result<bool,E>)->Result<(),E> {
    let (mut start,mut na,_)=stack[i];let (b,mut nb,_)=stack[i+1];
    stack[i].1+=nb;stack.remove(i+1);
    let skip=gallop(&a[b],&a[start..start+na],0,true,lt)?;
    start+=skip;na-=skip;
    if na==0 {return Ok(());}
    nb=gallop(&a[start+na-1],&a[b..b+nb],nb-1,false,lt)?;
    if nb==0 {return Ok(());}
    // Copies simplify ownership; only lt calls affect the symbolic trace.
    let left=a[start..start+na].to_vec();let right=a[b..b+nb].to_vec();
    let dest=&mut a[start..b+nb];
    if na<=nb {merge_lo(dest,&left,&right,mg,lt)} else {merge_hi(dest,&left,&right,mg,lt)}
}
fn merge_lo<T:Clone,E>(out:&mut [T],a:&[T],b:&[T],mg:&mut usize,
                       lt:&mut impl FnMut(&T,&T)->Result<bool,E>)->Result<(),E> {
    let mut i=0;let mut j=1;let mut d=1;
    out[0]=b[0].clone();let mut threshold=*mg;
    'outer: while j<b.len() && a.len()-i>1 {
        let mut ac=0;let mut bc=0;
        loop {
            if lt(&b[j],&a[i])? {
                out[d]=b[j].clone();j+=1;d+=1;bc+=1;ac=0;
                if j==b.len() {break 'outer;}
                if bc>=threshold {break;}
            } else {
                out[d]=a[i].clone();i+=1;d+=1;ac+=1;bc=0;
                if a.len()-i==1 {break 'outer;}
                if ac>=threshold {break;}
            }
        }
        threshold+=1;
        loop {
            threshold-=usize::from(threshold>1);*mg=threshold;
            ac=gallop(&b[j],&a[i..],0,true,lt)?;
            out[d..d+ac].clone_from_slice(&a[i..i+ac]);d+=ac;i+=ac;
            if a.len()-i<=1 {break 'outer;}
            out[d]=b[j].clone();d+=1;j+=1;
            if j==b.len() {break 'outer;}
            bc=gallop(&a[i],&b[j..],0,false,lt)?;
            out[d..d+bc].clone_from_slice(&b[j..j+bc]);d+=bc;j+=bc;
            if j==b.len() {break 'outer;}
            out[d]=a[i].clone();d+=1;i+=1;
            if a.len()-i==1 {break 'outer;}
            if ac<7 && bc<7 {break;}
        }
        threshold+=1;*mg=threshold;
    }
    if a.len()-i==1 && j<b.len() {
        let n=b.len()-j;out[d..d+n].clone_from_slice(&b[j..]);d+=n;
        out[d]=a[i].clone();
    } else {
        let n=a.len()-i;out[d..d+n].clone_from_slice(&a[i..]);d+=n;
        out[d..].clone_from_slice(&b[j..]);
    }
    Ok(())
}
fn merge_hi<T:Clone,E>(out:&mut [T],a:&[T],b:&[T],mg:&mut usize,
                       lt:&mut impl FnMut(&T,&T)->Result<bool,E>)->Result<(),E> {
    let mut i=a.len()-1;let mut j=b.len();let mut d=out.len()-1;
    out[d]=a[i].clone();let mut threshold=*mg;
    'outer: while i>0 && j>1 {
        let mut ac=0;let mut bc=0;
        loop {
            d-=1;
            if lt(&b[j-1],&a[i-1])? {
                i-=1;out[d]=a[i].clone();ac+=1;bc=0;
                if i==0 {break 'outer;}
                if ac>=threshold {break;}
            } else {
                j-=1;out[d]=b[j].clone();bc+=1;ac=0;
                if j==1 {break 'outer;}
                if bc>=threshold {break;}
            }
        }
        threshold+=1;
        loop {
            threshold-=usize::from(threshold>1);*mg=threshold;
            ac=i-gallop(&b[j-1],&a[..i],i-1,true,lt)?;
            out[d-ac..d].clone_from_slice(&a[i-ac..i]);d-=ac;i-=ac;
            if i==0 {break 'outer;}
            d-=1;j-=1;out[d]=b[j].clone();
            if j==1 {break 'outer;}
            bc=j-gallop(&a[i-1],&b[..j],j-1,false,lt)?;
            out[d-bc..d].clone_from_slice(&b[j-bc..j]);d-=bc;j-=bc;
            if j<=1 {break 'outer;}
            d-=1;i-=1;out[d]=a[i].clone();
            if i==0 {break 'outer;}
            if ac<7 && bc<7 {break;}
        }
        threshold+=1;*mg=threshold;
    }
    if j==1 && i>0 {
        out[1..i+1].clone_from_slice(&a[..i]);out[0]=b[0].clone();
    } else {
        out[..i].clone_from_slice(&a[..i]);out[i..i+j].clone_from_slice(&b[..j]);
    }
    Ok(())
}
