// Integer-only verifier: all numerical decisions use int64 / signed __int128.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <vector>
using I=int64_t; using W=__int128_t;
static I S,lo,H,C,T,D;
static uint64_t RC,RT,RD;
void setup(){RC=(uint64_t)((__uint128_t(1)<<64)/C);RT=T?(uint64_t)((__uint128_t(1)<<64)/T):0;RD=(uint64_t)((__uint128_t(1)<<64)/D);}
__attribute__((always_inline)) inline I fd(W a,I b){

 if(b==(I(1)<<42))return (I)(a>>42);
 if(b==(I(1)<<43))return (I)(a>>43);
 uint64_t recip=b==C?RC:(b==T?RT:RD);
 bool neg=a<0;__uint128_t aa=neg?-a:a;

 __uint128_t q=(aa*recip)>>64;
 __uint128_t rem=aa-q*(uint64_t)b;
 q+=(uint64_t)rem/(uint64_t)b;
 bool nonzero=(q*(uint64_t)b!=aa);

 return neg?-(I)q-nonzero:(I)q;
}
__attribute__((always_inline)) inline I cd(W a,I b){return -fd(-a,b);}
I muldn(I a,I b){return fd(W(a)*b,S);} I mulup(I a,I b){return cd(W(a)*b,S);}
struct R{I x,y,X,Y,rho,mass;};
std::vector<R> rect;
struct Edge{I l,h;};
Edge vertical(I x,I y,I Y,I a,I b){
 if(a<0||b<0)return {0,0};
 if(!T){if(x < -a||x>a)return {0,0};I z=std::max(I(0),std::min(Y,b)-std::max(y,-b));return {z,z};}
 W f=W(a)*D-W(C)*x,g=W(b)*D+W(T)*x;
 W ff=-W(a)*D-W(C)*x,gg=-W(b)*D+W(T)*x;
 I u=std::min({Y,fd(f,T),fd(g,C)}),v=std::max({y,cd(ff,T),cd(gg,C)});
 I U=std::min({Y,cd(f,T),cd(g,C)}),V=std::max({y,fd(ff,T),fd(gg,C)});
 return {std::max(I(0),u-v),std::max(I(0),U-V)};
}
Edge horizontal(I y,I x,I X,I a,I b){
 if(a<0||b<0)return {0,0};
 if(!T){if(y < -b||y>b)return {0,0};I z=std::max(I(0),std::min(X,a)-std::max(x,-a));return {z,z};}
 W f=W(a)*D-W(T)*y,g=W(C)*y+W(b)*D;
 W ff=-W(a)*D-W(T)*y,gg=W(C)*y-W(b)*D;
 I u=std::min({X,fd(f,C),fd(g,T)}),v=std::max({x,cd(ff,C),cd(gg,T)});
 I U=std::min({X,cd(f,C),cd(g,T)}),V=std::max({x,fd(ff,C),fd(gg,T)});
 return {std::max(I(0),u-v),std::max(I(0),U-V)};
}
I area(I x,I X,I y,I Y,I a,I b){
 if(a<=0||b<=0)return 0;
 if(!T)return muldn(std::max(I(0),std::min(X,a)-std::max(x,-a)),std::max(I(0),std::min(Y,b)-std::max(y,-b)));
 I ext=cd(W(C)*a+W(T)*b,D),ey=cd(W(T)*a+W(C)*b,D);
 x=std::max(x,-ext);X=std::min(X,ext);y=std::max(y,-ey);Y=std::min(Y,ey); if(x>=X||y>=Y)return 0;
 I xs[16];int n=0;xs[n++]=x;xs[n++]=X;
 auto add=[&](I v){if(v>x&&v<X)xs[n++]=v;};
 for(int i:{-1,1})for(int j:{-1,1}) add(fd(W(i)*C*a+W(j)*T*b,D));
 for(I yy:{y,Y})for(int i:{-1,1}){add(fd(W(i)*a*D-W(T)*yy,C));add(fd(W(C)*yy+W(i)*b*D,T));}
 std::sort(xs,xs+n); I A=0,prev=0;
 for(int i=0;i<n;i++){
   I xx=xs[i]; I top=std::min({Y,fd(W(a)*D-W(C)*xx,T),fd(W(b)*D+W(T)*xx,C)});
   I bot=std::max({y,cd(-W(a)*D-W(C)*xx,T),cd(-W(b)*D+W(T)*xx,C)});
   I len=top-bot;
   if(i && len+prev>0)A+=fd(W(xx-xs[i-1])*(len+prev),W(2)*S);
   prev=len;
 }
 return A;
}
struct Node{I x,y,X,Y,ins;int depth;std::vector<int> ids;I gx=0,gy=0;bool grad=false;};
int main(int argc,char**argv){
 if(argc!=2)return 2;FILE*f=fopen(argv[1],"r");assert(f);int nr,nd;long long ss,ll,hh;
 assert(fscanf(f,"%lld%lld%lld%d%d",&ss,&ll,&hh,&nr,&nd)==5);S=ss;lo=ll;H=hh;
 for(int i=0;i<nr;i++){long long x,y,X,Y,r;assert(fscanf(f,"%lld%lld%lld%lld%lld",&x,&y,&X,&Y,&r)==5);R q{ x,y,X,Y,r,0}; q.mass=muldn(r,muldn(X-x,Y-y));rect.push_back(q);}
 for(int k=0;k<nd;k++){
 int r;long long c,t,d,u;assert(fscanf(f,"%d%lld%lld%lld%lld",&r,&c,&t,&d,&u)==5);C=c;T=t;D=d;setup();
 clock_t start=clock();std::vector<Node> stack;Node root{lo,lo,u,u,0,0,{}};for(int i=0;i<nr;i++)root.ids.push_back(i);stack.push_back(std::move(root));
 long long nodes=0,leaves=0;I minbound=INT64_MAX,mincentre=INT64_MAX,argx=0,argy=0;bool ok=true;
 while(!stack.empty()){
 Node n=std::move(stack.back());stack.pop_back();nodes++;
 I px=(n.x+n.X)/2,py=(n.y+n.Y)/2,dx=std::max(px-n.x,n.X-px),dy=std::max(py-n.y,n.Y-py);
 I bu=cd(W(C)*dx+W(T)*dy,D),bv=cd(W(T)*dx+W(C)*dy,D),ins=n.ins,A=0,gxl=0,gxh=0,gyl=0,gyh=0;
 I am=H-bu,bm=H-bv,ap=H+bu,bp=H+bv;std::vector<int> keep;keep.reserve(n.ids.size());
 for(int id:n.ids){R q=rect[id];I x=q.x-px,X=q.X-px,y=q.y-py,Y=q.Y-py;
 W umin=W(C)*x+W(T)*y,umax=W(C)*X+W(T)*Y,vmin=-W(T)*X+W(C)*y,vmax=-W(T)*x+W(C)*Y;
 if(umin>=-W(am)*D && umax<=W(am)*D && vmin>=-W(bm)*D && vmax<=W(bm)*D){ins+=q.mass;continue;}
 if(umin>W(ap)*D||umax<-W(ap)*D||vmin>W(bp)*D||vmax<-W(bp)*D)continue;
 I ext=cd(W(C+T)*H,D);if(x>ext+dx||X < -ext-dx||y>ext+dy||Y < -ext-dy)continue;
 keep.push_back(id);A+=muldn(q.rho,area(x,X,y,Y,H,H));
 }
 I centre=ins+A;
 I bound=n.grad?centre-mulup(n.gx,dx)-mulup(n.gy,dy):-INT64_MAX;
 I Gx=n.gx,Gy=n.gy;
 if(bound<S){
 for(int id:keep){R q=rect[id];I x=q.x-px,X=q.X-px,y=q.y-py,Y=q.Y-py;
 auto l=vertical(x,y,Y,am,bm),L=vertical(x,y,Y,ap,bp),rr=vertical(X,y,Y,am,bm),RR=vertical(X,y,Y,ap,bp);
 auto b=horizontal(y,x,X,am,bm),B=horizontal(y,x,X,ap,bp),tt=horizontal(Y,x,X,am,bm),TT=horizontal(Y,x,X,ap,bp);
 gxl+=muldn(q.rho,l.l-RR.h);gxh+=mulup(q.rho,L.h-rr.l);gyl+=muldn(q.rho,b.l-TT.h);gyh+=mulup(q.rho,B.h-tt.l);
 }
 I gx=std::max(std::abs(gxl),std::abs(gxh)),gy=std::max(std::abs(gyl),std::abs(gyh));
 Gx=n.grad?std::min(n.gx,gx):gx;Gy=n.grad?std::min(n.gy,gy):gy;
 bound=centre-mulup(Gx,dx)-mulup(Gy,dy);
 }
 if(bound<S){
 I E=0;for(int id:keep){R q=rect[id];E+=muldn(q.rho,area(q.x-px,q.X-px,q.y-py,q.Y-py,am,bm));}
 bound=std::max(bound,ins+E);
 }
 if(centre<mincentre){mincentre=centre;argx=px;argy=py;}
 if(bound>=S){leaves++;minbound=std::min(minbound,bound);continue;}
 if(centre<S-S/100000 || n.depth>=90 || nodes>10000000){ok=false;printf("{\"candidate\":%d,\"centre_lower_units\":%lld,\"x_units\":%lld,\"y_units\":%lld}\n",r,(long long)centre,(long long)px,(long long)py);break;}
 Node a{n.x,n.y,n.X,n.Y,ins,n.depth+1,keep},b=a;a.gx=b.gx=Gx;a.gy=b.gy=Gy;a.grad=b.grad=true;
 if(n.X-n.x>=n.Y-n.y){a.X=px;b.x=px;}else{a.Y=py;b.y=py;}
 stack.push_back(std::move(b));stack.push_back(std::move(a));
 }
 printf("{\"r\":%d,\"verdict\":\"%s\",\"nodes\":%lld,\"leaves\":%lld,\"scale\":%lld,\"min_bound_units\":%lld,\"min_centre_lower_units\":%lld,\"arg_units\":[%lld,%lld],\"cpu_seconds\":%.3f}\n",r,ok?"VERIFIED":"REFUSED",nodes,leaves,(long long)S,(long long)minbound,(long long)mincentre,(long long)argx,(long long)argy,(double)(clock()-start)/CLOCKS_PER_SEC);fflush(stdout);
 }
 fclose(f);return 0;
}
