#include <cstdint>
#include <cstring>
// 连续姿态区间验证；数学内核沿用 Tokoharu 的平移导数，凹截面法参考 Squares Project。
// Continuous-pose interval verification; translation derivatives follow Tokoharu, concave sections follow the Squares Project.
// 新增连续半正切参数、相关表达式与精确旋转宽度外包；不是完全独立的代码来源。
// Adds continuous half-tangents, correlated expressions and exact extent enclosures; code lineage is not wholly independent.
#if defined(NDEBUG) || defined(__FAST_MATH__)
#error "Assertions and IEEE semantics are required"
#endif
#if defined(__SSE__)
#include <xmmintrin.h>
#endif
#include <algorithm>
#include <array>
#include <cassert>
#include <cfenv>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>
#include <chrono>
using namespace std;
// IEEE 正负数的编码有序，故整数加减一给出相邻浮点数。
// IEEE encodings are ordered by sign, so adding or subtracting one gives the neighbor.
inline double step_up(double x){
    if(isnan(x))return nextafter(x,INFINITY);
    if(x==INFINITY)return x;
    if(x==0)return numeric_limits<double>::denorm_min();
    uint64_t v;memcpy(&v,&x,8);v=x>0?v+1:v-1;memcpy(&x,&v,8);return x;
}
inline double dn(double x){return -step_up(-x);}
inline double up(double x){return step_up(x);}
struct I {double l,h; I(double x=0):l(x),h(x){} I(double a,double b):l(a),h(b){} double mid()const{return l+(h-l)/2;}};
I operator+(I a,I b){return {dn(a.l+b.l),up(a.h+b.h)};}
I operator-(I a,I b){return {dn(a.l-b.h),up(a.h-b.l)};}
I operator-(I a){return {-a.h,-a.l};}
I operator*(I a,I b){double x[]={a.l*b.l,a.l*b.h,a.h*b.l,a.h*b.h};return {dn(*min_element(x,x+4)),up(*max_element(x,x+4))};}
I operator/(I a,I b){assert(b.l>0 || b.h<0);return a*I(dn(1/b.h),up(1/b.l));}
I mn(I a,I b){return {min(a.l,b.l),min(a.h,b.h)};} I mx(I a,I b){return {max(a.l,b.l),max(a.h,b.h)};}
I pos(I a){return {max(0.,a.l),max(0.,a.h)};} I ab(I a){return a.l>=0?a:(a.h<=0?-a:I(0,max(-a.l,a.h)));}
I readI(istream&in){string a,b;in>>a>>b;assert(in);double x=stod(a),y=stod(b);assert(isfinite(x)&&isfinite(y)&&x<=y);return {x,y};}
struct R {I a,b,d,e,rho;};
struct Coeff {I hs,hc,cs,sc;double cf,sf,hf;};
Coeff frame;
I angle_c,angle_s,halfB,angle_extent;
inline double mul_dn_pos(I k,double x){return dn((x>=0?k.l:k.h)*x);}
inline double mul_up_pos(I k,double x){return up((x>=0?k.h:k.l)*x);}

inline double signed_section(double x,double e,double b){
    I xi(x),top(e),bottom(b);
    I cx=angle_c*xi,sx=angle_s*xi;
    I f1=(halfB-cx)/angle_s,f2=(halfB+sx)/angle_c;
    I g1=(-halfB-cx)/angle_s,g2=(-halfB+sx)/angle_c;
    return (mn(top,mn(f1,f2))-mx(bottom,mx(g1,g2))).l;
}

double area_lower(const R&r,I cx,I cy,I c,I s,I B){
    double left=up(r.a.h-cx.l),right=dn(r.d.l-cx.h);
    double top=dn(r.e.l-cy.h),bottom=up(r.b.h-cy.l);
    if(left>=right || bottom>=top)return 0;
    double cc=frame.cf,ss=frame.sf,h=frame.hf;
    double candidates[]={h*(cc-ss),-h*(cc-ss),(h-ss*top)/cc,(cc*top-h)/ss,
        -(h+ss*bottom)/cc,(cc*bottom+h)/ss,h*(cc+ss),-h*(cc+ss),
        -(h+ss*top)/cc,(cc*top+h)/ss,(h-ss*bottom)/cc,(cc*bottom-h)/ss};
    double knots[14];int n=2;knots[0]=left;knots[1]=right;
    for(double x:candidates)if(left<x && x<right)knots[n++]=x;
    sort(knots,knots+n);
    double sum=0,prev=signed_section(knots[0],top,bottom);
    for(int k=1;k<n;k++){
        double v=signed_section(knots[k],top,bottom),vsum=dn(prev+v),width=dn(knots[k]-knots[k-1]);
        if(vsum>0 && width>0)sum=dn(sum+dn(dn(vsum*width)*.5));
        prev=v;
    }
    return max(0.,sum);
}

I slice_correlated(I z,I C,I O,I lo,I hi,I c,I s,I h){
    I off=z-C,cx=c*off,sx=s*off;
    I top=O+mn((h-cx)/s,(h+sx)/c);
    I bottom=O+mx((-h-cx)/s,(-h+sx)/c);
    return pos(mn(hi,top)-mx(lo,bottom));
}
struct Bound {double lower,fx,fy,center;};
Bound bound(double u,double v,double du,double dv,I L,I B,I c,I s,const vector<R>&rs){
    I ex=B*angle_extent/I(2),E=L/I(2)-ex,cx=L/I(2)+I(u)*E,cy=L/I(2)+I(v)*E,dx=I(du)*E,dy=I(dv)*E;
    I X(cx.l-dx.h,cx.h+dx.h),Y(cy.l-dy.h,cy.h+dy.h);X={dn(X.l),up(X.h)};Y={dn(Y.l),up(Y.h)};
    I xb=X-ex,xt=X+ex,yb=Y-ex,yt=Y+ex;
    I fx(0),fy(0);double f=0;
    for(const auto&r:rs){
        if(r.d.h<=xb.l || r.a.l>=xt.h || r.e.h<=yb.l || r.b.l>=yt.h)continue;
        f=dn(f+dn(r.rho.l*area_lower(r,cx,cy,c,s,B)));
        I a(0),b(0),d(0),e(0);
        if(r.a.h>=xb.l && r.a.l<=xt.h)a=slice_correlated(r.a,X,Y,r.b,r.e,c,s,B/I(2));
        if(r.d.h>=xb.l && r.d.l<=xt.h)b=slice_correlated(r.d,X,Y,r.b,r.e,c,s,B/I(2));
        if(r.b.h>=yb.l && r.b.l<=yt.h)d=slice_correlated(r.b,Y,X,r.a,r.d,s,c,B/I(2));
        if(r.e.h>=yb.l && r.e.l<=yt.h)e=slice_correlated(r.e,Y,X,r.a,r.d,s,c,B/I(2));
        fx=fx+r.rho*(a-b);fy=fy+r.rho*(d-e);
    }
    double rx=up(dx.h*ab(fx).h),ry=up(dy.h*ab(fy).h);
    return {dn(dn(f-rx)-ry),rx,ry,f};
}

struct Node {double u,v,du,dv,base; int depth; vector<R> active; double w,dw;};
struct Classified {vector<R> active; double base; long long inside=0,outside=0;};

Classified classify(const Node&n,I L,I B,I c,I s){
    I ex=B*angle_extent/I(2),E=L/I(2)-ex;
    I cx=L/I(2)+I(n.u)*E,cy=L/I(2)+I(n.v)*E,dx=I(n.du)*E,dy=I(n.dv)*E;
    I X(dn(cx.l-dx.h),up(cx.h+dx.h)),Y(dn(cy.l-dy.h),up(cy.h+dy.h));
    I xb=X-ex,xt=X+ex,yb=Y-ex,yt=Y+ex;
    double cc=c.mid(),ss=s.mid(),hh=B.mid()/2,xx=cx.mid(),yy=cy.mid();
    double eu=cc*dx.h+ss*dy.h,ev=ss*dx.h+cc*dy.h;
    Classified out;out.base=n.base;out.active.reserve(n.active.size());
    for(const auto&r:n.active){
        if(r.d.h<=xb.l || r.a.l>=xt.h || r.e.h<=yb.l || r.b.l>=yt.h){out.outside++;continue;}
        double rx0=(r.a.mid()+r.d.mid())/2-xx,ry0=(r.b.mid()+r.e.mid())/2-yy;
        double hx0=(r.d.mid()-r.a.mid())/2,hy0=(r.e.mid()-r.b.mid())/2;
        double au=abs(cc*rx0+ss*ry0),av=abs(-ss*rx0+cc*ry0),wu=cc*hx0+ss*hy0,wv=ss*hx0+cc*hy0;
        bool maybe_in=au+wu+eu<=hh+1e-10 && av+wv+ev<=hh+1e-10;
        bool maybe_out=au-wu-eu>=hh-1e-10 || av-wv-ev>=hh-1e-10;
        // 容差仅提出候选，不能作任何接受判据。\n        // Tolerance only proposes a candidate and never decides acceptance.
        if(maybe_in||maybe_out){
            I rx=(r.a+r.d)/I(2)-X,ry=(r.b+r.e)/I(2)-Y,hx=(r.d-r.a)/I(2),hy=(r.e-r.b)/I(2);
            I U=ab(c*rx+s*ry),V=ab(-s*rx+c*ry),WU=c*hx+s*hy,WV=s*hx+c*hy;
            if(maybe_in && (U+WU).h<=(B/I(2)).l && (V+WV).h<=(B/I(2)).l){
                out.base=dn(out.base+max(0.,(r.rho*(r.d-r.a)*(r.e-r.b)).l));out.inside++;continue;
            }
            if(maybe_out && ((U-WU).l>=(B/I(2)).h || (V-WV).l>=(B/I(2)).h)){out.outside++;continue;}
        }
        out.active.push_back(r);
    }
    return out;
}


struct Direction{I c,s,extent;};
Direction direction(I T){
    assert(0<T.l && T.h<=.5);
    I low(T.l),high(T.h),one(1),two(2);
    I ca=(one-high*high)/(one+high*high),cb=(one-low*low)/(one+low*low);
    I sa=two*low/(one+low*low),sb=two*high/(one+high*high);
    
    I wa=(one+two*low-low*low)/(one+low*low),wb=(one+two*high-high*high)/(one+high*high);
    double wlo=min(wa.l,wb.l),whi=max(wa.h,wb.h);
    I aa=low*low+two*low-one,bb=high*high+two*high-one;
    if(aa.l<=0 && bb.h>=0)whi=(I(1414213562373096.)/I(1000000000000000.)).h;
    return {{ca.l,cb.h},{sa.l,sb.h},{wlo,whi}};
}
void set_frame(I B,Direction d){angle_c=d.c;angle_s=d.s;halfB=B/I(2);angle_extent=d.extent;frame={B/(I(2)*d.s),B/(I(2)*d.c),d.c/d.s,d.s/d.c,d.c.mid(),d.s.mid(),(B/I(2)).l};}
double center_mass(const Node&n,I L,I B,Direction d){
    I E=L/I(2)-B*angle_extent/I(2),cx=L/I(2)+I(n.u)*E,cy=L/I(2)+I(n.v)*E;
    double f=n.base;for(const auto&r:n.active)f=dn(f+dn(r.rho.l*area_lower(r,cx,cy,d.c,d.s,B)));return f;
}
int main(int argc,char**argv){
    static_assert(numeric_limits<double>::is_iec559 && sizeof(double)==8);assert(fegetround()==FE_TONEAREST);
    
#if defined(__SSE__)
    assert((_mm_getcsr() & ((1u<<15)|(1u<<6)))==0);
#endif
    assert(argc>=6);long long pl=stoll(argv[1]),ph=stoll(argv[2]),den=stoll(argv[3]),tn=stoll(argv[4]),td=stoll(argv[5]);
    long long maxnodes=argc>6?stoll(argv[6]):2000000;
    assert(0<pl && pl<ph && ph<=den/2 && den<=10000000 && tn>0 && td>0 && tn<100000000 && td<100000000);
    I T0=I(double(pl))/I(double(den)),span=I(double(ph-pl))/I(double(den));
    const double threshold=up(double(tn)/double(td));
    ifstream in("certificate_input.txt");assert(in);I L=readI(in),B=readI(in);int nr;in>>nr;vector<R>rs;
    for(int i=0;i<nr;i++){R r;r.a=readI(in);r.b=readI(in);r.d=readI(in);r.e=readI(in);r.rho=readI(in);assert(r.rho.l>=0);rs.push_back(r);}
    assert(in && nr>0 && nr<=10000 && 0<B.l && B.h<L.l && L.h<10);
    auto start=chrono::steady_clock::now();long long nodes=0,leaves=0,inside=0,outside=0,active_sum=0,angle_splits=0;int max_depth=0;double minbound=INFINITY;
    vector<Node>stack; stack.push_back({.5,.5,.5,.5,0.,0,rs,.5,.5});cout<<setprecision(17);
    while(!stack.empty()){
        Node z=move(stack.back());stack.pop_back();nodes++;max_depth=max(max_depth,z.depth);
        I T=T0+span*I(z.w-z.dw,z.w+z.dw);Direction d=direction(T);set_frame(B,d);
        auto cl=classify(z,L,B,d.c,d.s);z.active=move(cl.active);z.base=cl.base;inside+=cl.inside;outside+=cl.outside;
        active_sum+=z.active.size();
        Bound b=bound(z.u,z.v,z.du,z.dv,L,B,d.c,d.s,z.active);b.lower=dn(b.lower+z.base);b.center=dn(b.center+z.base);
        assert(isfinite(b.lower)&&isfinite(b.fx)&&isfinite(b.fy)&&isfinite(b.center));
        if(b.lower>=threshold){leaves++;minbound=min(minbound,b.lower);continue;}
        if(nodes>=maxnodes || min(min(z.du,z.dv),z.dw)<0x1p-40){
            cout<<"{\"status\":\"unresolved\",\"nodes\":"<<nodes<<",\"leaves\":"<<leaves<<",\"u\":"<<z.u<<",\"v\":"<<z.v<<",\"w\":"<<z.w<<",\"du\":"<<z.du<<",\"dv\":"<<z.dv<<",\"dw\":"<<z.dw<<",\"center_lower\":"<<b.center<<",\"angle_splits\":"<<angle_splits<<",\"max_depth\":"<<max_depth<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}"<<endl;return 3;
        }
        Direction dm=direction(T0+span*I(z.w));set_frame(B,dm);
        double midpoint=center_mass(z,L,B,dm),angle_loss=max(0.,midpoint-b.center);
        Node other=z;z.depth++;other.depth++;
        if(angle_loss>=max(b.fx,b.fy)){
            z.dw/=2;other.dw=z.dw;z.w-=z.dw;other.w+=z.dw;angle_splits++;
        }else if(b.fx>=b.fy){z.du/=2;other.du=z.du;z.u-=z.du;other.u+=z.du;}
        else{z.dv/=2;other.dv=z.dv;z.v-=z.dv;other.v+=z.dv;}
        stack.push_back(move(z));stack.push_back(move(other));
    }
    double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
    cout<<"{\"status\":\"verified\",\"pl\":"<<pl<<",\"ph\":"<<ph<<",\"den\":"<<den<<",\"nodes\":"<<nodes<<",\"leaves\":"<<leaves<<",\"lower_bound\":"<<minbound<<",\"seconds\":"<<sec<<",\"full_inside\":"<<inside<<",\"full_outside\":"<<outside<<",\"mean_active\":"<<double(active_sum)/nodes<<",\"max_depth\":"<<max_depth<<",\"angle_splits\":"<<angle_splits<<"}"<<endl;
}
