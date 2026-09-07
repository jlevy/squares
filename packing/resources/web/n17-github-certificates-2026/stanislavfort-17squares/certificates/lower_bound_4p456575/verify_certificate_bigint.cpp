#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>

using boost::multiprecision::cpp_int;
static constexpr std::int64_t Q = (std::int64_t{1} << 40);
static constexpr std::int64_t XS = 1000000 * Q;
static constexpr std::int64_t LS = 4456575 * Q;
static constexpr std::int64_t LO = 500000 * Q;
static constexpr std::int64_t HI = 3956575 * Q;
static constexpr std::int64_t DEN = 1'000'000;
struct Pt { std::int64_t x,y; };
static constexpr std::array<Pt,16> P{{
 {963374,984985},{1581796,985592},{2476851,926473},{3456650,919147},
 {995406,1792837},{1990669,1796975},{2972834,1793954},{3523331,1792554},
 {922136,2657284},{1491209,2660029},{2483245,2665147},{3456650,2667556},
 {999352,3529848},{1962693,3518471},{2850255,3462543},{3456920,3456650},
}};
struct B { std::int64_t xl,xh,yl,yh,tl,th; unsigned depth; };
static cpp_int ab(const cpp_int& z) { return z<0 ? -z : z; }
static std::int64_t minabs(const B& b) {
  if (b.tl<=0 && b.th>=0) return 0;
  auto a=b.tl<0?-b.tl:b.tl, c=b.th<0?-b.th:b.th;
  return std::min(a,c);
}
static bool a_lt_h(std::int64_t anum,std::int64_t unum) {
  if (anum<0) return true;
  cpp_int A=anum,U=unum,S=Q,X=XS;
  return 4*A*A*(S*S+U*U) < X*X*(S+U)*(S+U);
}
static bool infeasible(const B& b) {
  auto u=minabs(b);
  return a_lt_h(b.xh,u)||a_lt_h(LS-b.xl,u)||a_lt_h(b.yh,u)||a_lt_h(LS-b.yl,u);
}
static cpp_int mn4(const cpp_int&a,const cpp_int&b,const cpp_int&c,const cpp_int&d) {
  return std::min(std::min(a,b),std::min(c,d));
}
static cpp_int mx4(const cpp_int&a,const cpp_int&b,const cpp_int&c,const cpp_int&d) {
  return std::max(std::max(a,b),std::max(c,d));
}
static bool covers(const B& b,const Pt& p) {
  const cpp_int dxl=cpp_int(p.x)*XS-cpp_int(b.xh)*DEN;
  const cpp_int dxh=cpp_int(p.x)*XS-cpp_int(b.xl)*DEN;
  const cpp_int dyl=cpp_int(p.y)*XS-cpp_int(b.yh)*DEN;
  const cpp_int dyh=cpp_int(p.y)*XS-cpp_int(b.yl)*DEN;
  const cpp_int t0=b.tl,t1=b.th;
  const cpp_int lo1=mn4(t0*dyl,t0*dyh,t1*dyl,t1*dyh);
  const cpp_int hi1=mx4(t0*dyl,t0*dyh,t1*dyl,t1*dyh);
  const cpp_int A0=dxl*Q+lo1, A1=dxh*Q+hi1;
  const cpp_int MA=std::max(ab(A0),ab(A1));
  const cpp_int nt0=-t1,nt1=-t0;
  const cpp_int lo2=mn4(nt0*dxl,nt0*dxh,nt1*dxl,nt1*dxh);
  const cpp_int hi2=mx4(nt0*dxl,nt0*dxh,nt1*dxl,nt1*dxh);
  const cpp_int B0=lo2+dyl*Q, B1=hi2+dyh*Q;
  const cpp_int MB=std::max(ab(B0),ab(B1));
  const cpp_int U=minabs(b),S=Q,X=XS,D=DEN;
  const cpp_int R=(S*S+U*U)*D*D*X*X;
  return 4*MA*MA<R && 4*MB*MB<R;
}
static std::pair<B,B> divide(const B& b,int d) {
  B a=b,c=b; ++a.depth;++c.depth;
  if(d==0){auto m=(b.xl+b.xh)/2;if(m==b.xl||m==b.xh)std::abort();a.xh=m;c.xl=m;}
  else if(d==1){auto m=(b.yl+b.yh)/2;if(m==b.yl||m==b.yh)std::abort();a.yh=m;c.yl=m;}
  else {auto m=(b.tl+b.th)/2;if(m==b.tl||m==b.th)std::abort();a.th=m;c.tl=m;}
  return {a,c};
}
[[noreturn]] static void bad(const char* msg,std::uint64_t n){std::cerr<<"BIGINT_INVALID node="<<n<<" "<<msg<<"\n";std::exit(1);}
int main(int argc,char**argv){
 const std::string path=argc>1?argv[1]:"square17_lb_4p456575.cert";
 std::ifstream f(path,std::ios::binary);if(!f){std::cerr<<"open failed\n";return 2;}
 std::vector<B> st{{LO,HI,LO,HI,-Q,Q,0}};
 std::uint64_t nodes=0,leaf=0,split=0;unsigned md=0;
 while(!st.empty()){
   B b=st.back();st.pop_back();int q=f.get();if(q==EOF)bad("early eof",nodes+1);
   unsigned op=(unsigned char)q;++nodes;md=std::max(md,b.depth);
   if(op==0){if(!infeasible(b))bad("bad infeasible",nodes);++leaf;}
   else if(op<=16){if(!covers(b,P[op-1]))bad("bad witness",nodes);++leaf;}
   else if(op<=19){auto [a,c]=divide(b,op-17);st.push_back(c);st.push_back(a);++split;}
   else bad("bad opcode",nodes);
 }
 if(f.get()!=EOF)bad("trailing data",nodes+1);
 if(leaf!=split+1)bad("not full tree",nodes);
 std::cout<<"BIGINT_CERTIFICATE_VALID\nL=4456575/1000000\nnodes="<<nodes<<"\nleaves="<<leaf<<"\nsplit="<<split<<"\nmax_depth="<<md<<"\n";
}
