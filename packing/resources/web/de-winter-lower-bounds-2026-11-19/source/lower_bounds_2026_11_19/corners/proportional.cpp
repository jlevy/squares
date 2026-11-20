// Integer verification of segment coverage with an outer support-intersection test.
#include <algorithm>
#include <vector>
#include <fstream>
#include <iostream>
#include <cstdint>
#include <string>
using I=int64_t;using W=__int128_t;constexpr I G=1LL<<28, DS=1LL<<30, MASS=1LL<<40, AQ=10000000;
I flo(W x,W y){if(y<0){x=-x;y=-y;}W z=x>=0?x/y:-((-x+y-1)/y);constexpr W m=W(1)<<55;return I(std::max(-m,std::min(m,z)));}
I cei(W x,W y){return -flo(-x,y);}
struct Row{I vert,lo,hi,fl,fh,den;};
struct Box{I x,y,X,Y;};
std::vector<Row> lines;W nx[24],ny[24],caprow[24];int normals;I nodes,leaves,minbound,depthmax,stop=1500000;
I segment(const Row&r,I x,I y){
 I lo=r.lo,hi=r.hi;
 for(int i=0;i<normals;i++){
  W u=r.vert?ny[i]:nx[i],v=r.vert?nx[i]:ny[i];I cx=r.vert?y:x,cy=r.vert?x:y;
  W b=v*((v>0?r.fh:r.fl)-cy);
  if(u>0)hi=std::min(hi,cx+flo(caprow[i]-b,u));
  else if(u<0)lo=std::max(lo,cx+cei(caprow[i]-b,u));
  else if(b>caprow[i])return 0;
  if(hi<=lo)return 0;
 }
 return flo(W(hi-lo)*r.den*MASS,W(G)*DS);
}
std::vector<Box> removed;
I skipped;
struct Added{Box xy; I relative, absolute;};
std::vector<Added> points;
std::vector<I> removed_cost;
I possible_fraction(const Box& off,const Box& seg){
 bool vertical=seg.X-seg.x<seg.Y-seg.y;
 I lo=vertical?seg.y:seg.x,hi=vertical?seg.Y:seg.X,den=std::max<I>(1,hi-lo-2);
 I translo=vertical?seg.x:seg.y,transhi=vertical?seg.X:seg.Y;
 I oxl=vertical?off.y:off.x,oxh=vertical?off.Y:off.X,oyl=vertical?off.x:off.y,oyh=vertical?off.X:off.Y;
 // A true intersection requires at least one nonpositive Bernstein coefficient on each face.
 // The convex hull of their allowed parameter intervals encloses the union.
 for(int j=0;j<4;j++){
  I l=hi+1,h=lo-1;
  for(int k=5*j;k<5*j+5;k++){
   W u=vertical?ny[k]:nx[k],v=vertical?nx[k]:ny[k];
   W right=caprow[k]+u*(u>0?oxh:oxl)+v*(v>0?oyh:oyl)-v*(v>0?translo:transhi);
   I a=lo,b=hi;
   if(u>0)b=std::min(b,cei(right,u));else if(u<0)a=std::max(a,flo(right,u));else if(right<0)continue;
   if(b<a)continue;l=std::min(l,a);h=std::max(h,b);
  }
  lo=l;hi=h;if(hi<=lo)return 0;
 }
 return std::min(MASS,cei(W(hi-lo)*MASS,den));
}
bool contains(const Box& offset,const Box& point) {
 for(int k=0;k<normals;k++) {
  I dx=nx[k]>=0 ? point.X-offset.x : point.x-offset.X;
  I dy=ny[k]>=0 ? point.Y-offset.y : point.y-offset.Y;
  if(nx[k]*dx+ny[k]*dy>caprow[k])return false;
 }
 return true;
}
bool cover(Box b,int dep){
 if(++nodes>stop||dep>62)return false;depthmax=std::max(depthmax,I(dep));
 W loss=0;I bonus=0,gain=0;
 for(size_t j=0;j<removed.size();j++)loss+=W(possible_fraction(b,removed[j]))*removed_cost[j];
 for(const Added& point:points) if(contains(b,point.xy)) {bonus+=point.absolute;gain+=point.relative;}
 if(W(gain)*MASS>=loss){leaves++;skipped++;return true;}
 I sums[4]={};I px[]={b.x,b.X,b.x,b.X},py[]={b.y,b.y,b.Y,b.Y};
 for(auto&r:lines){
  I vals[4];bool ok=true;
  for(int j=0;j<4;j++){vals[j]=segment(r,px[j],py[j]);if(!vals[j]){ok=false;break;}}
  if(ok)for(int j=0;j<4;j++)sums[j]+=vals[j];
 }
 I low=bonus+*std::min_element(sums,sums+4);
 if(low>=MASS){minbound=std::min(minbound,low);leaves++;return true;}
 if(std::max(b.X-b.x,b.Y-b.y)<=4){std::cerr<<"unresolved "<<b.x<<" "<<b.y<<" "<<low<<"\n";return false;}
 Box a=b,d=b;
 if(b.X-b.x>=b.Y-b.y){I mid=b.x+(b.X-b.x)/2;a.X=mid;d.x=mid;}else{I mid=b.y+(b.Y-b.y)/2;a.Y=mid;d.y=mid;}
 return cover(a,dep+1)&&cover(d,dep+1);
}
int main(int argc,char**argv){
 if(argc!=2)return 2;std::ifstream in(argv[1]);int n;in>>n;if(n<=0||n>4000)return 2;
 for(int i=0;i<n;i++){Row r;in>>r.vert>>r.lo>>r.hi>>r.fl>>r.fh>>r.den;
  if(!in||r.vert<0||r.vert>1||r.lo<0||r.hi>4*G||r.fl<0||r.fh>4*G||r.den<0||r.den>1000LL*DS)return 2;
  lines.push_back(r);}
 int nr;in>>nr;if(!in||nr<=0||nr>1000)return 2;
 for(int j=0;j<nr;j++){Box z;in>>z.x>>z.y>>z.X>>z.Y;if(!in||z.x<0||z.y<0||z.X<z.x||z.Y<z.y||z.X>2*G||z.Y>2*G)return 2;removed.push_back(z);}
 for(int j=0;j<nr;j++){I w;in>>w;if(!in||w<=0||w>(1LL<<48))return 2;removed_cost.push_back(w);}
 int count;in>>count;if(!in||count<0||count>1000)return 2;
 for(int j=0;j<count;j++){Added p;in>>p.xy.x>>p.xy.y>>p.xy.X>>p.xy.Y>>p.relative>>p.absolute;
 if(!in||p.xy.x<0||p.xy.y<0||p.xy.X>3*G||p.xy.Y>3*G||p.xy.x>p.xy.X||p.xy.y>p.xy.Y||p.relative<0||p.relative>(1LL<<48)||p.absolute<0||p.absolute>10*MASS)return 2;points.push_back(p);}
 I id;Box box;while(std::cin>>id>>normals>>box.x>>box.y>>box.X>>box.Y){
  if(normals!=20||box.x<0||box.y<0||box.X>3*G||box.Y>3*G||box.x>box.X||box.y>box.Y)return 2;
  for(int i=0;i<normals;i++){I x,y,z;std::cin>>x>>y>>z;if(!std::cin||std::max({std::abs(x),std::abs(y),std::abs(z)})>(1LL<<61))return 2;nx[i]=x;ny[i]=y;caprow[i]=W(z)*G;}
  nodes=0;leaves=0;skipped=0;depthmax=0;minbound=INT64_MAX;
  bool ok=cover(box,0);std::cout<<id<<" "<<(ok?"PASS":"OPEN")<<" "<<nodes<<" "<<leaves<<" "<<depthmax<<" "<<(ok?minbound:0)<<" "<<skipped<<"\n";
 }return 0;
}
