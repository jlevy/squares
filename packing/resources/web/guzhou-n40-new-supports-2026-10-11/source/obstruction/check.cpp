// 有理多边形裁剪的固定轨道族上限检查；不使用数值 LP 作证明。
// Fixed-orbit-family obstruction by rational polygon clipping; numerical LP is not proof.
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/rational.hpp>
#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <string>
#include <stdexcept>
#include <algorithm>
#include <chrono>
using Z=boost::multiprecision::cpp_int;
using Q=boost::rational<Z>;
void need(bool b,const char*s){if(!b)throw std::runtime_error(s);}
Q readq(std::istream&in){std::string s;in>>s;need(bool(in),"INPUT");auto p=s.find('/');return p==std::string::npos?Q(Z(s)):Q(Z(s.substr(0,p)),Z(s.substr(p+1)));}
struct Rect{Q a,b,c,d;};struct V{Q x,y;};
Q absq(Q x){return x<0?-x:x;}
Q intersection(Rect r,Q cx,Q cy,Q c,Q s,Q h,Q extent,long long&part){
 if(r.c<=cx-extent||r.a>=cx+extent||r.d<=cy-extent||r.b>=cy+extent)return Q(0);
 r={r.a-cx,r.b-cy,r.c-cx,r.d-cy};
 Q u0=c*r.a+s*r.b,u1=c*r.c+s*r.d,v0=-s*r.c+c*r.b,v1=-s*r.a+c*r.d;
 if(u0>=h||u1<=-h||v0>=h||v1<=-h)return Q(0);
 if(u0>=-h&&u1<=h&&v0>=-h&&v1<=h)return (r.c-r.a)*(r.d-r.b);
 part++;
 std::vector<V> poly{{r.a,r.b},{r.c,r.b},{r.c,r.d},{r.a,r.d}};
 std::array<V,4> ns{{{c,s},{-s,c},{-c,-s},{s,-c}}};
 for(const auto&normal:ns){
  if(poly.size()<3)return Q(0);std::vector<V> out;
  for(size_t j=0;j<poly.size();++j){
   const V&v=poly[j];const V&u=poly[(j+poly.size()-1)%poly.size()];
   Q fu=h-normal.x*u.x-normal.y*u.y,fv=h-normal.x*v.x-normal.y*v.y;
   if((fu>=0)!=(fv>=0)){Q t=fu/(fu-fv);out.push_back({u.x+t*(v.x-u.x),u.y+t*(v.y-u.y)});}
   if(fv>=0)out.push_back(v);
  }
  poly.swap(out);
 }
 if(poly.size()<3)return Q(0);Q area(0);const V&anchor=poly[0];
 for(size_t j=1;j+1<poly.size();++j)area+=(poly[j].x-anchor.x)*(poly[j+1].y-anchor.y)-(poly[j+1].x-anchor.x)*(poly[j].y-anchor.y);
 return absq(area)/Q(2);
}
int main(int argc,char**argv){try{
 need(argc==2,"USAGE_INPUT");std::ifstream in(argv[1]);Q L=readq(in),B=readq(in);int n,m;in>>n>>m;
 need(L==Q(67,10)&&B==Q(335,336)&&n==2526&&0<m&&m<=1000,"FAMILY_SCOPE");
 std::vector<std::array<Rect,8>> sites(n);std::vector<Q> areas(n);
 for(int j=0;j<n;++j){Rect r{readq(in),readq(in),readq(in),readq(in)};need(0<=r.a&&r.a<r.c&&r.c<=L&&0<=r.b&&r.b<r.d&&r.d<=L,"RECT");areas[j]=Q(8)*(r.c-r.a)*(r.d-r.b);int k=0;
  for(int reflect=0;reflect<2;++reflect){Rect z=reflect?Rect{L-r.c,r.b,L-r.a,r.d}:r;for(int turn=0;turn<4;++turn){sites[j][k++]=z;z={L-z.d,z.a,L-z.b,z.c};}}
 }
 struct Pose{Q u,v,t;Z w;};std::vector<Pose>poses;Z sum=0;
 for(int i=0;i<m;++i){Pose p{readq(in),readq(in),readq(in),Z(0)};in>>p.w;need(in&&p.w>0&&p.u>=0&&p.u<=1&&p.v>=0&&p.v<=1&&p.t>=0&&p.t<=Q(1,2),"POSE");poses.push_back(p);sum+=p.w;}
 std::string extra;need(!(in>>extra),"TRAILING_INPUT");const Z scale("1000000000000");std::vector<Z> scores(n,Z(0));long long partial=0;auto start=std::chrono::steady_clock::now();
 for(int i=0;i<m;++i){const auto&p=poses[i];Q c=(Q(1)-p.t*p.t)/(Q(1)+p.t*p.t),s=Q(2)*p.t/(Q(1)+p.t*p.t),h=B/Q(2),extent=h*(c+s),E=L/Q(2)-extent,cx=L/Q(2)+p.u*E,cy=L/Q(2)+p.v*E;need(E>0,"CENTER_DOMAIN");
  for(int j=0;j<n;++j){Q area(0);for(const auto&r:sites[j])area+=intersection(r,cx,cy,c,s,h,extent,partial);Q coefficient=area/areas[j];need(coefficient>=0&&coefficient<=1,"COEFFICIENT");Q scaled=coefficient*Q(scale);Z rounded=(scaled.numerator()+scaled.denominator()-1)/scaled.denominator();scores[j]+=p.w*rounded;}
  if((i+1)%25==0)std::cerr<<"poses "<<i+1<<"/"<<m<<"\n";
 }
 auto it=std::max_element(scores.begin(),scores.end());Z maximum=*it,denom=sum*scale,slack=denom-40*maximum;bool pass=slack>0;
 std::cout<<"{\"status\":\""<<(pass?"EXACT_FAMILY_OBSTRUCTION":"DUAL_REFUSED")<<"\",\"sites\":"<<n<<",\"poses\":"<<m<<",\"max_column\":"<<(it-scores.begin())<<",\"max_score_numerator\":\""<<maximum<<"\",\"max_score_denominator\":\""<<denom<<"\",\"strict_scaled_slack\":\""<<slack<<"\",\"partial_clippings\":"<<partial<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}"<<std::endl;
 return pass?0:2;
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 3;}}
