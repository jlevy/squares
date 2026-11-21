#include <algorithm>
#include <array>
#include <cstdint>
#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using I=std::int64_t;
using W=__int128_t;
struct Rect{I x,y,X,Y,w;};
struct Change{I x;int lo,hi,k;I amount;};
struct Segment{I x,y,X,Y,w;int k;};
std::string digits(W n){if(n<10)return std::to_string((int)n);return digits(n/10)+char('0'+n%10);}
W envelope(std::vector<Rect> const& rs,I T,I x0,I y0,I x1,I y1,bool mirror_x,bool mirror_y,bool omit_far=false){
 std::vector<Segment> parts;std::vector<I> ys{y0,y1};W simple=0;
 for(auto r:rs)for(int i=0;i<=int(mirror_x);i++)for(int j=0;j<=int(mirror_y);j++){
  if(omit_far&&i&&j)continue;
  I x=std::max(x0,i?T-r.X:r.x),X=std::min(x1,i?T-r.x:r.X);
  I y=std::max(y0,j?T-r.Y:r.y),Y=std::min(y1,j?T-r.y:r.Y);
  if(x>=X||y>=Y)continue;
  if(!mirror_x&&!mirror_y)simple+=W(X-x)*(Y-y)*r.w;
  else{parts.push_back({x,y,X,Y,r.w,2*i+j});ys.push_back(y);ys.push_back(Y);}
 }
 if(!mirror_x&&!mirror_y)return simple;
 std::sort(ys.begin(),ys.end());ys.erase(std::unique(ys.begin(),ys.end()),ys.end());
 std::vector<Change> changes;
 for(auto a:parts){
  int lo=std::lower_bound(ys.begin(),ys.end(),a.y)-ys.begin(),hi=std::lower_bound(ys.begin(),ys.end(),a.Y)-ys.begin();
  changes.push_back({a.x,lo,hi,a.k,a.w});changes.push_back({a.X,lo,hi,a.k,-a.w});
 }
 std::sort(changes.begin(),changes.end(),[](auto &a,auto &b){return a.x<b.x;});
 std::vector<std::array<I,4>> diff(ys.size(),{0,0,0,0});W sum=0;size_t q=0;
 while(q<changes.size()){
  I x=changes[q].x;
  while(q<changes.size()&&changes[q].x==x){
   auto c=changes[q++];diff[c.lo][c.k]+=c.amount;diff[c.hi][c.k]-=c.amount;
  }
  if(q==changes.size())break;
  W column=0;std::array<I,4> density{};
  for(size_t j=0;j+1<ys.size();j++){
   for(int k=0;k<4;k++)density[k]+=diff[j][k];
   column+=W(*std::max_element(density.begin(),density.end()))*(ys[j+1]-ys[j]);
  }
  sum+=column*(changes[q].x-x);
 }
 return sum;
}
int main(int argc,char**argv){
 if(argc<3)return 1;constexpr I G=10000000,r=7071070;I S,count;std::ifstream input(argv[1]);input>>S>>count;
 if(!input||S<=0||S>20*G||count<=0||count>1000000)return 2;
 std::vector<Rect> rs(count);W sum_density=0;
 for(auto &z:rs){input>>z.x>>z.y>>z.X>>z.Y>>z.w;
  if(!input||z.x<0||z.y<0||z.X>S||z.Y>S||z.x>=z.X||z.y>=z.Y||z.w<0)return 3;sum_density+=z.w;
 }
 if(sum_density>(W(1)<<59))return 4;
 for(int i=2;i<argc;i++){
  std::string arg(argv[i]);auto split=arg.find('@'),disk=arg.find('~');I T=std::stoll(arg),mid=T/2;
  int steps=disk==std::string::npos?0:std::stoi(arg.substr(disk+1));
  if(steps<0||steps>128||(steps&&split!=std::string::npos))return 6;
  I seam=split==std::string::npos?mid:std::stoll(arg.substr(split+1));
  if(T<=0||T>40*G||T%2||std::min(seam,T-seam)<=r||std::max(seam,T-seam)+r>S)return 5;
  W total=0;
  if(seam==mid){
   I cut=mid-r;
   W core=envelope(rs,T,0,0,cut,cut,false,false);
   W edge=envelope(rs,T,cut,0,mid,cut,true,false);
   W center=0;
   if(!steps)center=envelope(rs,T,cut,cut,mid,mid,true,true);
   else for(int k=0;k<steps;k++){
    I a=cut+k*r/steps,b=cut+(k+1)*r/steps;
    I gap=mid-b,rad=std::max<I>(0,G*G/2-gap*gap),reach=static_cast<I>(std::sqrt(static_cast<long double>(rad)));
    while(reach*reach<rad)++reach;
    while(reach>0&&(reach-1)*(reach-1)>=rad)--reach;
    I split_y=std::max(cut,mid-reach);
    center+=envelope(rs,T,a,cut,b,split_y,true,true,true);
    center+=envelope(rs,T,a,split_y,b,mid,true,true);
   }
   total=4*(core+2*edge+center);
  }else{
   std::array<I,3> lo{0,seam-r,0},hi{seam-r,seam+r,T-seam-r};
   for(int u=0;u<3;u++)for(int v=0;v<=u;v++)
    total+=(u==v?1:2)*envelope(rs,T,lo[u],lo[v],hi[u],hi[v],u==1,v==1);
  }
  std::cout<<arg<<" "<<digits(total)<<"\n";
 }
}
