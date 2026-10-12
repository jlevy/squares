// Method-distinct axis coverage: integer hinge expansions and 2D prefix sums.
// All arithmetic decisions are exact. Input safety is checked before accumulation.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Z = __int128_t;
using I = int64_t;
std::string text(Z x) { if(x==0) return "0"; bool neg=x<0; if(neg)x=-x; std::string s; while(x){s.push_back(char('0'+x%10));x/=10;} if(neg)s.push_back('-'); std::reverse(s.begin(),s.end());return s; }
void require(bool b,const char* s){if(!b)throw std::runtime_error(s);}
struct Rect {I a,b,d,e,w;};
int main(int argc,char**argv){try{
 require(argc==2,"Usage: axis_integer_grid INPUT"); std::ifstream in(argv[1]);require(bool(in),"Input unavailable");
 I l,B,G,P,tau_num,tau_den;size_t n;in>>l>>B>>G>>P>>tau_num>>tau_den>>n;
 require(in && 0<B && B<l && l<=10000000000LL && G>0 && G<=1000000000LL && P>0 && P<=1000000000LL && tau_num>0 && tau_num<=1000000 && tau_den>0 && tau_den<=1000000 && n<=10000,"Input bounds");
 require(l%2==0 && B%2==0,"Half units must be integral");
 std::vector<Rect> rs(n);std::vector<I> xs{l/2,l-B/2},ys=xs;Z weights=0;
 for(auto&r:rs){in>>r.a>>r.b>>r.d>>r.e>>r.w; require(in && 0<=r.a && r.a<r.d && r.d<=l && 0<=r.b && r.b<r.e && r.e<=l && 0<=r.w && r.w<=1000000000000000LL,"Rectangle bounds");weights+=r.w;
  for(I x:{r.a-B/2,r.a+B/2,r.d-B/2,r.d+B/2})if(l/2<=x && x<=l-B/2)xs.push_back(x);
  for(I y:{r.b-B/2,r.b+B/2,r.e-B/2,r.e+B/2})if(l/2<=y && y<=l-B/2)ys.push_back(y);
 }
 std::string extra;require(!(in>>extra),"Trailing input");
 for(auto*v:{&xs,&ys}){std::sort(v->begin(),v->end());v->erase(std::unique(v->begin(),v->end()),v->end());}
 size_t nx=xs.size(),ny=ys.size();require(nx*ny<=15000000,"Grid too large");
 // Each of 16 signed hinge pairs per rectangle contributes to each coefficient.
 // max |knot| <= l+B/2. Accumulation, evaluation, and threshold comparisons
 // are bounded well inside signed 128-bit arithmetic by these explicit guards.
 Z maxk=l+B/2;
 require(weights<Z(1000000000000000LL),"Total coefficient bound");
 Z eval_bound=16*weights*(Z(l)+maxk)*(Z(l)+maxk);
 require(eval_bound < (Z(1)<<125),"Coefficient/evaluation overflow guard");
 std::array<std::vector<Z>,4> coef;for(auto&v:coef)v.resize(nx*ny,0);
 const I signs[]={1,-1,-1,1};
 for(const auto&r:rs){I kx[]={r.a-B/2,r.a+B/2,r.d-B/2,r.d+B/2};I ky[]={r.b-B/2,r.b+B/2,r.e-B/2,r.e+B/2};
  for(int u=0;u<4;u++)for(int v=0;v<4;v++){
   size_t i=std::lower_bound(xs.begin(),xs.end(),kx[u])-xs.begin(),j=std::lower_bound(ys.begin(),ys.end(),ky[v])-ys.begin();if(i==nx||j==ny)continue;
   size_t pos=i*ny+j;Z w=Z(r.w)*signs[u]*signs[v];
   coef[0][pos]+=w;coef[1][pos]-=w*ky[v];coef[2][pos]-=w*kx[u];coef[3][pos]+=w*kx[u]*ky[v];
  }
 }
 for(auto&v:coef){
  for(size_t i=1;i<nx;i++)for(size_t j=0;j<ny;j++)v[i*ny+j]+=v[(i-1)*ny+j];
  for(size_t i=0;i<nx;i++)for(size_t j=1;j<ny;j++)v[i*ny+j]+=v[i*ny+j-1];
 }
 Z minimum=(Z(1)<<125);size_t mi=0,mj=0;
 for(size_t i=0;i<nx;i++)for(size_t j=0;j<ny;j++){
  size_t p=i*ny+j;Z z=coef[0][p]*xs[i]*ys[j]+coef[1][p]*xs[i]+coef[2][p]*ys[j]+coef[3][p];
  require(z>=0,"Negative capture: invalid computation");if(z<minimum){minimum=z;mi=i;mj=j;}
 }
 Z direct=0;
 for(const auto&r:rs){I dx=std::max(I(0),std::min(r.d,xs[mi]+B/2)-std::max(r.a,xs[mi]-B/2));I dy=std::max(I(0),std::min(r.e,ys[mj]+B/2)-std::max(r.b,ys[mj]-B/2));direct+=Z(r.w)*dx*dy;}
 require(direct==minimum,"Minimizer direct-sum reconciliation");
 Z scale=Z(P)*G*G;
 // Divide before comparison: avoids multiplying the large minimum by tau_den.
 Z required=(scale*tau_num+tau_den-1)/tau_den;
 bool pass=minimum>=required;
 std::cout<<"{\"status\":\""<<(pass?"AXIS_COVERAGE_PROVED":"AXIS_TEST_REFUSED")<<"\",\"x_nodes\":"<<nx<<",\"y_nodes\":"<<ny<<",\"minimum_numerator\":\""<<text(minimum)<<"\",\"scale\":\""<<text(scale)<<"\",\"minimizer_x_integer\":"<<xs[mi]<<",\"minimizer_y_integer\":"<<ys[mj]<<",\"direct_sum_matches\":true,\"evaluation_abs_bound\":\""<<text(eval_bound)<<"\"}\n";
 return pass?0:2;
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 3;}}
