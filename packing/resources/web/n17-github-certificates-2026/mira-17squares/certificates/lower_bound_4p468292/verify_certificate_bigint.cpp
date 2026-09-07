#include <algorithm>
#include <array>
#include <boost/multiprecision/cpp_int.hpp>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <vector>

using boost::multiprecision::cpp_int;
constexpr std::int64_t ST = (std::int64_t{1} << 40);
constexpr std::int64_t SX = 1'000'000 * ST;
constexpr std::int64_t PD = 10'000'000;
constexpr std::int64_t LNUM = 4'468'292;
constexpr std::int64_t LS = LNUM * ST;
constexpr std::int64_t LO = 500'000 * ST;
constexpr std::int64_t HI = (LNUM - 500'000) * ST;

struct Point { std::int64_t x,y; };
constexpr std::array<Point,16> P{{
 {9633740,9849850},{16317845,9829523},{25287879,9446006},{34682923,9443212},
 {9999997,17580956},{19993909,17929744},{29988027,18272588},{35451063,18219620},
 {9172158,26508741},{14694893,26410332},{24689011,26753176},{34682923,27101964},
 {9999997,35239708},{19395041,35236914},{28365087,34853407},{34687946,34687946},
}};
struct Tri { int a,b,c; };
constexpr std::array<Tri,18> TR{{
 {0,1,4},{1,2,5},{1,4,5},{2,3,6},{2,5,6},{3,6,7},
 {4,5,9},{4,8,9},{5,6,10},{5,9,10},{6,7,11},{6,10,11},
 {8,9,12},{9,10,13},{9,12,13},{10,11,14},{10,13,14},{11,14,15}
}};
struct Box {std::int64_t x0,x1,y0,y1,t0,t1; unsigned depth;};

cpp_int ab(const cpp_int& x){ return x < 0 ? -x : x; }
std::int64_t min_abs_t(const Box& b){ if(b.t0<=0&&b.t1>=0)return 0; return std::min(std::llabs(b.t0),std::llabs(b.t1)); }
bool half(std::int64_t a,std::int64_t u){ if(a<0)return true; cpp_int A=a,U=u,T=ST,X=SX; return 4*A*A*(T*T+U*U)<X*X*(T+U)*(T+U); }
bool infeasible(const Box& b){ auto u=min_abs_t(b); return half(b.x1,u)||half(LS-b.x0,u)||half(b.y1,u)||half(LS-b.y0,u); }

bool covers(const Point& p,const Box& b){
 cpp_int dx0=cpp_int(p.x)*SX-cpp_int(b.x1)*PD,dx1=cpp_int(p.x)*SX-cpp_int(b.x0)*PD;
 cpp_int dy0=cpp_int(p.y)*SX-cpp_int(b.y1)*PD,dy1=cpp_int(p.y)*SX-cpp_int(b.y0)*PD;
 std::array<cpp_int,4> q{{cpp_int(b.t0)*dy0,cpp_int(b.t0)*dy1,cpp_int(b.t1)*dy0,cpp_int(b.t1)*dy1}};
 auto mm=std::minmax_element(q.begin(),q.end()); cpp_int a0=dx0*ST+*mm.first,a1=dx1*ST+*mm.second,ma=std::max(ab(a0),ab(a1));
 q={{cpp_int(-b.t1)*dx0,cpp_int(-b.t1)*dx1,cpp_int(-b.t0)*dx0,cpp_int(-b.t0)*dx1}};
 mm=std::minmax_element(q.begin(),q.end()); cpp_int b0=*mm.first+dy0*ST,b1=*mm.second+dy1*ST,mb=std::max(ab(b0),ab(b1));
 cpp_int U=min_abs_t(b),T=ST,X=SX,D=PD,rhs=(T*T+U*U)*D*D*X*X;
 return 4*ma*ma<rhs && 4*mb*mb<rhs;
}

cpp_int cross(const Point&a,const Point&b,const Point&c){return cpp_int(b.x-a.x)*(c.y-a.y)-cpp_int(b.y-a.y)*(c.x-a.x);}
bool edges(const Tri&t){int v[3]={t.a,t.b,t.c};for(int i=0;i<3;++i)for(int j=i+1;j<3;++j){cpp_int dx=cpp_int(P[v[i]].x)-P[v[j]].x,dy=cpp_int(P[v[i]].y)-P[v[j]].y;if(dx*dx+dy*dy>=cpp_int(PD)*PD)return false;}return true;}
cpp_int edge(const Point&a,const Point&b,std::int64_t x,std::int64_t y){cpp_int ex=b.x-a.x,ey=b.y-a.y,rx=cpp_int(x)*PD-cpp_int(a.x)*SX,ry=cpp_int(y)*PD-cpp_int(a.y)*SX;return ex*ry-ey*rx;}
bool triangle(int index,const Box&b){Tri t=TR[index];if(!edges(t))return false;if(cross(P[t.a],P[t.b],P[t.c])<0)std::swap(t.b,t.c);for(auto x:{b.x0,b.x1})for(auto y:{b.y0,b.y1}){if(edge(P[t.a],P[t.b],x,y)<=0||edge(P[t.b],P[t.c],x,y)<=0||edge(P[t.c],P[t.a],x,y)<=0)return false;}return true;}

std::pair<Box,Box> split(Box b,int d){Box a=b,c=b;a.depth=c.depth=b.depth+1;if(d==0){auto m=(b.x0+b.x1)/2;if(m==b.x0||m==b.x1)throw std::runtime_error("x exhausted");a.x1=m;c.x0=m;}else if(d==1){auto m=(b.y0+b.y1)/2;if(m==b.y0||m==b.y1)throw std::runtime_error("y exhausted");a.y1=m;c.y0=m;}else if(d==2){auto m=(b.t0+b.t1)/2;if(m==b.t0||m==b.t1)throw std::runtime_error("t exhausted");a.t1=m;c.t0=m;}else throw std::runtime_error("bad split");return{a,c};}

int main(int argc,char**argv){
 std::string path=argc>1?argv[1]:"square17_lb_4p468292.cert";std::ifstream in(path,std::ios::binary);if(!in){std::cerr<<"cannot open certificate\n";return 2;}std::vector<unsigned char> cert((std::istreambuf_iterator<char>(in)),{});
 std::vector<Box> st{{LO,HI,LO,HI,-ST,ST,0}};std::size_t cur=0;std::uint64_t nodes=0,splits=0,cov=0,tris=0,inf=0;unsigned md=0;
 try{while(!st.empty()){if(cur>=cert.size())throw std::runtime_error("early EOF");unsigned op=cert[cur++];Box b=st.back();st.pop_back();++nodes;md=std::max(md,b.depth);if(op==0){if(!infeasible(b))throw std::runtime_error("false infeasible");++inf;}else if(op<=16){if(op==0||!covers(P[op-1],b))throw std::runtime_error("false point");++cov;}else if(op<=19){auto ac=split(b,op-17);st.push_back(ac.second);st.push_back(ac.first);++splits;}else if(op<20+TR.size()){if(!triangle(op-20,b))throw std::runtime_error("false triangle");++tris;}else throw std::runtime_error("unknown opcode");}if(cur!=cert.size())throw std::runtime_error("trailing bytes");if(cov+tris+inf!=splits+1)throw std::runtime_error("not full tree");}
 catch(const std::exception&e){std::cerr<<"BIGINT_CERTIFICATE_REJECTED node="<<nodes<<" "<<e.what()<<"\n";return 1;}
 std::cout<<"BIGINT_CERTIFICATE_VALID_4P468292\nL=4468292/1000000\nnodes="<<nodes<<"\nsplit="<<splits<<"\ncovered="<<cov<<"\ntriangle="<<tris<<"\ninfeasible="<<inf<<"\nmax_depth="<<md<<"\n";
}
