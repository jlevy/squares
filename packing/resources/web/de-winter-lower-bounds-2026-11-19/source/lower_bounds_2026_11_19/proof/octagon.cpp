// Independent certificate checker. Floating point proposes vertices only.
// Every accepted mass bound is proved with integer comparisons and areas.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <vector>
using I=std::int64_t;
using W=__int128_t;
constexpr I G=I(1)<<30, U=I(1)<<24, M=U*U, DS=I(1)<<32;
struct P{I x,y;bool operator<(const P&q)const{return x!=q.x?x<q.x:y<q.y;}bool operator==(const P&q)const{return x==q.x&&y==q.y;}};
struct Fp{double x,y;};
struct Rect{I x0,y0,x1,y1,X0,Y0,X1,Y1,den,m;};
struct Box{I x0,y0,x1,y1;};
I C,H,E;W threshold;double c,s,side;
std::vector<Rect> rs; long long nodes=0,clips=0,leaves=0,cap=3000000;
I least=std::numeric_limits<I>::max(); int maxdepth=0;
W cross(P a,P b,P d){return W(b.x-a.x)*(d.y-a.y)-W(b.y-a.y)*(d.x-a.x);}
W ab(W a){return a<0?-a:a;}
I isqrt(I x){I y=std::sqrt(double(x));while(W(y)*y>x)y--;while(W(y+1)*(y+1)<=x)y++;return y;}
constexpr I AQ=10000000;
std::array<W,4> nx,ny;std::array<double,4> fx,fy;W ocap;
bool enclosed(const Rect&r,const Box&b){
  I xl=r.X0-b.x1,xh=r.X1-b.x0,yl=r.Y0-b.y1,yh=r.Y1-b.y0;
  for(int k=0;k<4;k++){
    W u=nx[k],v=ny[k];
    W lo=u*(u>=0?xl:xh)+v*(v>=0?yl:yh);
    W hi=u*(u>=0?xh:xl)+v*(v>=0?yh:yl);
    if(lo < -ocap || hi > ocap)return false;
  }
  return true;
}
bool within(const Rect&r,I px,I py,P v){
  if(v.x<r.x0||v.x>r.x1||v.y<r.y0||v.y>r.y1)return false;
  I x=v.x-px,y=v.y-py;
  for(int k=0;k<4;k++)if(ab(nx[k]*x+ny[k]*y)>ocap)return false;
  return true;
}
I area_mass(W area2,const Rect&r){
 // area2 uses units G^-2, den uses units DS^-1. All factors are nonnegative.
 return (I)((area2*W(r.den))/(W(2)*G*G/(M/DS)));
}
I clipped_mass(const Rect&r,I px,I py){
 // Clip in a slightly smaller polygon, then check every proposed lattice vertex
 // against the exact true half-planes. Failure to propose a vertex only weakens the bound.
 double x0=double(r.x0-px)+2,y0=double(r.y0-py)+2,x1=double(r.x1-px)-2,y1=double(r.y1-py)-2;
 if(x0>=x1||y0>=y1)return 0;
 Fp poly[16]={{x0,y0},{x1,y0},{x1,y1},{x0,y1}},tmp[16];int len=4;
 double normals[8][2];for(int k=0;k<4;k++){normals[2*k][0]=fx[k];normals[2*k][1]=fy[k];normals[2*k+1][0]=-fx[k];normals[2*k+1][1]=-fy[k];}
 for(auto &axis:normals){
  if(!len)return 0;int k=0;Fp prev=poly[len-1];double a=prev.x*axis[0]+prev.y*axis[1]-side;
  for(int t=0;t<len;t++){
   Fp curr=poly[t];double b=curr.x*axis[0]+curr.y*axis[1]-side;
   if((a<=0)!=(b<=0)){double u=a/(a-b);tmp[k++]={prev.x+u*(curr.x-prev.x),prev.y+u*(curr.y-prev.y)};}
   if(b<=0)tmp[k++]=curr;prev=curr;a=b;
  }
  len=k;std::copy(tmp,tmp+k,poly);
 }
 if(len<3)return 0;
 P angles[16],hull[32];int n=0;
 for(int k=0;k<len;k++){
  P v={px+std::llround(poly[k].x),py+std::llround(poly[k].y)};
  if(within(r,px,py,v))angles[n++]=v;
 }
 if(n<3)return 0;
 // Floating-point polygon order cannot affect the count. Use an integer convex hull.
 std::sort(angles,angles+n);n=std::unique(angles,angles+n)-angles;if(n<3)return 0;int k=0;
 for(int j=0;j<n;j++){while(k>=2&&cross(hull[k-2],hull[k-1],angles[j])<=0)k--;hull[k++]=angles[j];}
 for(int j=n-2,b=k+1;j>=0;j--){while(k>=b&&cross(hull[k-2],hull[k-1],angles[j])<=0)k--;hull[k++]=angles[j];}
 W a=0;for(int j=1;j+1<k-1;j++)a+=cross(hull[0],hull[j],hull[j+1]);
 return area_mass(a,r);
}
struct CacheEntry { I px=0,py=0,value=0;int rid=-1; };
constexpr unsigned cache_size=1u<<19;
static std::vector<CacheEntry> cache(cache_size);
static std::uint64_t mix(std::uint64_t x) {
 x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;return x^(x>>31);
}
I mass(int id,const Rect&r,I px,I py){
 auto key=mix(std::uint64_t(px)*19379771ULL^std::uint64_t(py)*736859ULL^std::uint64_t(id)*863891151ULL);
 auto &ent=cache[key&(cache_size-1)];
 if(ent.rid==id&&ent.px==px&&ent.py==py)return ent.value;
 // A fast rejection is conservative since it discards nonnegative mass. A full
 // contribution always needs the exact integer enclosure test below.
 double lx=r.X0-px,hx=r.X1-px,ly=r.Y0-py,hy=r.Y1-py;
 double u0=c*lx+s*ly,u1=c*hx+s*hy,v0=-s*hx+c*ly,v1=-s*lx+c*hy;
 I val=0;
 if(u0<side+8&&u1>-side-8&&v0<side+8&&v1>-side-8){
  if(u0>=-side-4&&u1<=side+4&&v0>=-side-4&&v1<=side+4&&enclosed(r,{px,py,px,py}))val=r.m;
  else val=clipped_mass(r,px,py);
 }
 ent={px,py,val,id};return val;
}
bool decide(Box b,const std::vector<int>&src,I inherited,int depth){
 if(++nodes>cap||depth>65)return false;maxdepth=std::max(maxdepth,depth);
 I full=inherited,add[4]={};std::vector<int> rem;rem.reserve(src.size());
 I ps[4][2]={{b.x0,b.y0},{b.x1,b.y0},{b.x0,b.y1},{b.x1,b.y1}};
 // An overly aggressive exclusion can only remove nonnegative mass.
 const double radius=(c+s)*side+8;
 const double pad=16;double xmin=b.x0-radius-pad,xmax=b.x1+radius+pad,ymin=b.y0-radius-pad,ymax=b.y1+radius+pad;
 for(int id:src){
  const Rect&r=rs[id];if(r.X1<xmin||r.X0>xmax||r.Y1<ymin||r.Y0>ymax)continue;
  if(enclosed(r,b)){full+=r.m;continue;}rem.push_back(id);
  if(b.x1-b.x0>G/3||b.y1-b.y0>G/3)continue;
  I v[4];bool ok=true;
  for(int j=0;j<4;j++){I val=mass(id,r,ps[j][0],ps[j][1]);clips++;if(val<=0){ok=false;break;}v[j]=isqrt(val);}
  if(!ok)continue;
  I a=(v[0]+v[1]+v[2]+v[3])/4;
  for(int j=0;j<4;j++)add[j]+=2*a*v[j]-a*a;
 }
 I bound=full+*std::min_element(add,add+4);
 if(bound>=M){leaves++;least=std::min(least,bound);return true;}
 if(std::max(b.x1-b.x0,b.y1-b.y0)<=1){std::cerr<<"unresolved "<<b.x0<<" "<<b.y0<<" bound "<<bound<<"\n";return false;}
 Box u=b,v=b;
 if(b.x1-b.x0>=b.y1-b.y0){I k=b.x0+(b.x1-b.x0)/2;u.x1=k;v.x0=k;}
 else {I k=b.y0+(b.y1-b.y0)/2;u.y1=k;v.y0=k;}
 return decide(u,rem,full,depth+1)&&decide(v,rem,full,depth+1);
}
int main(int argc,char**argv){
 if(argc!=4)return 2;std::ifstream in(argv[1]),dir(argv[2]);cap=std::atoll(argv[3]);int k;in>>k;
 if(!in||k<=0||k>16000)return 2;rs.resize(k);I total=0;
 for(auto&r:rs){in>>r.x0>>r.y0>>r.x1>>r.y1>>r.X0>>r.Y0>>r.X1>>r.Y1>>r.den>>r.m;
  if(!in||r.X0<0||r.Y0<0||r.X1>20*G||r.Y1>20*G||r.den<0||r.m<0||r.m>M*4)return 2;
  // Bound all products, including the area * density conversion and the sum of affine supports.
  W rect2=W(2)*(r.X1-r.X0)*(r.Y1-r.Y0);
  if(rect2<0||((rect2*r.den)/(W(2)*G*G/(M/DS)))>W(5)*M)return 2;
  total+=r.m;
 }
 if(total>400*M)return 2;
 I Twhole,Trem;Box b;dir>>C>>H>>E>>Twhole>>Trem>>b.x0>>b.y0>>b.x1>>b.y1;
 if(!dir||C<=0||H<0||E<=0||C>E||H>E||E>10000000000000LL||Twhole<0||Twhole>G||Trem<0||Trem>=E)return 2;
 threshold=W(Twhole)*E+Trem;c=double(C)/E;s=double(H)/E;side=Twhole+double(Trem)/E-3;
 I num;dir>>num;
 if(!dir||num<=0||num>AQ/20||Twhole!=G/2||Trem!=0 || ab(W(C)*C+W(H)*H-W(E)*E)!=0)return 2;
 // The intersection of |u| + num/AQ |v| <= 1/2 and its transpose.
 // Conservative broad-phase rejections may discard mass only.
 nx={W(AQ)*C-W(num)*H,W(AQ)*C+W(num)*H,-W(AQ)*H+W(num)*C,-W(AQ)*H-W(num)*C};
 ny={W(AQ)*H+W(num)*C,W(AQ)*H-W(num)*C,W(AQ)*C+W(num)*H,W(AQ)*C-W(num)*H};
 ocap=W(E)*AQ*(G/2);
 for(int j=0;j<4;j++){fx[j]=double(nx[j])/(double(E)*AQ);fy[j]=double(ny[j])/(double(E)*AQ);}
 std::vector<int> inds(k);std::iota(inds.begin(),inds.end(),0);
 bool ok=decide(b,inds,0,0);
 std::cout<<(ok?"PASS":"UNDECIDED")<<" "<<nodes<<" "<<leaves<<" "<<clips<<" "<<maxdepth<<" "<<(ok?least:0)<<"\n";
 return ok?0:1;
}
