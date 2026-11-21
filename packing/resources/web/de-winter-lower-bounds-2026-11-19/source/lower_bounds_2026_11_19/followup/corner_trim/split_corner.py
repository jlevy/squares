from fractions import Fraction as F
def split_rows(data,corner):
    side=F(data['L'])
    result=[]
    for row in data['rectangles']:
        a,b,A,B=xy=tuple(map(F,row['rectangle']))
        if max(min(A,side-a),min(B,side-b))>corner or max(A-a,B-b)<=F(1,5):
            result.append(row)
            continue
        horizontal=A-a>=B-b
        low,high=(a,A) if horizontal else (b,B)
        step=(high-low)/3
        weight=str(F(row['mass'])/3)
        for j in range(3):
            u,v=low+j*step,low+(j+1)*step
            coords=(u,b,v,B) if horizontal else (a,u,A,v)
            result.append(dict(rectangle=list(map(str,coords)),mass=weight))
    return dict(data,rectangles=result)
