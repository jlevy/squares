#include <boost/multiprecision/cpp_int.hpp>
#include <omp.h>
#include <algorithm>
#include <atomic>
#include <charconv>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
using Integer=boost::multiprecision::cpp_int;
constexpr int kGrid=4000;
constexpr int kSideNumerator=9141;
constexpr int kSideDenominator=2000;
constexpr std::int64_t kCoverageTarget=1'000'000'000'000LL;
constexpr std::size_t kExpectedAtoms=560;
constexpr std::size_t kExpectedSamples=148937;
constexpr std::int64_t kExpectedMass=16'994'734'834'452LL;
struct Atom{int x,y;std::int64_t w;};
struct Sample{Integer p,q;};
struct Rect{Integer l,r,b,t;std::int64_t w;};
struct Event{int l,r;std::int64_t d;};
struct Audit{bool ok;std::uint64_t runs;std::int64_t mincov;};
Integer ab(const Integer&x){return x<0?-x:x;}
std::vector<std::string> split(const std::string&s){std::vector<std::string>f;std::string c;for(char x:s){if(x==','){f.push_back(c);c.clear();}else c.push_back(x);}f.push_back(c);return f;}
long long pll(const std::string&s){long long v=0;auto [p,e]=std::from_chars(s.data(),s.data()+s.size(),v);if(e!=std::errc{}||p!=s.data()+s.size())throw std::runtime_error("bad integer "+s);return v;}
std::vector<Atom> load_atoms(const std::string&p){std::ifstream in(p);if(!in)throw std::runtime_error("cannot open atoms");std::string line;std::getline(in,line);std::vector<Atom>a;std::int64_t mass=0;while(std::getline(in,line)){if(line.empty())continue;auto f=split(line);if(f.size()!=4)throw std::runtime_error("bad atom row");Atom z{(int)pll(f[0]),(int)pll(f[1]),pll(f[3])};a.push_back(z);mass+=z.w;}if(a.size()!=kExpectedAtoms)throw std::runtime_error("atom count");if(mass!=kExpectedMass)throw std::runtime_error("mass mismatch "+std::to_string(mass));return a;}
std::vector<Sample> load_samples(const std::string&p){std::ifstream in(p);if(!in)throw std::runtime_error("cannot open samples");std::vector<Sample>s;std::string a,b;while(in>>a>>b){Sample z{Integer(a),Integer(b)};if(z.p<=0||z.q<=0)throw std::runtime_error("bad sample");if(z.p*z.p+2*z.p*z.q-z.q*z.q>=0)throw std::runtime_error("sample endpoint");if(!s.empty()&&s.back().p*z.q>=z.p*s.back().q)throw std::runtime_error("sample order");s.push_back(std::move(z));}if(s.size()!=kExpectedSamples)throw std::runtime_error("sample count "+std::to_string(s.size()));return s;}
int exact_index(const std::vector<Integer>&v,const Integer&x){auto it=std::lower_bound(v.begin(),v.end(),x);if(it==v.end()||*it!=x)throw std::runtime_error("edge missing");return int(it-v.begin());}

bool intersects(const Integer&left,const Integer&right,const Integer&bottom,const Integer&top,const Integer&cu,const Integer&cv,const Integer&extent,const Integer&proj,const Integer&c,const Integer&s){
 Integer width=right-left,height=top-bottom,du=left+right-2*cu,dv=bottom+top-2*cv;
 Integer g1=ab(du)-width-2*extent,g2=ab(dv)-height-2*extent;
 Integer g3=ab(du*c-dv*s)-(proj+width*c+height*s);
 Integer g4=ab(du*s+dv*c)-(proj+width*s+height*c);
 return std::max(std::max(g1,g2),std::max(g3,g4))<=0;
}

struct SegTree{
 int n;std::vector<std::int64_t>mn,mx,lazy;
 explicit SegTree(int n_):n(n_),mn(4*n_,0),mx(4*n_,0),lazy(4*n_,0){}
 void apply(int p,std::int64_t d){mn[p]+=d;mx[p]+=d;lazy[p]+=d;}
 void push(int p){if(lazy[p]){apply(2*p,lazy[p]);apply(2*p+1,lazy[p]);lazy[p]=0;}}
 void pull(int p){mn[p]=std::min(mn[2*p],mn[2*p+1]);mx[p]=std::max(mx[2*p],mx[2*p+1]);}
 void add(int l,int r,std::int64_t d){if(l<r)add(1,0,n,l,r,d);}
 void add(int p,int l,int r,int ql,int qr,std::int64_t d){if(qr<=l||r<=ql)return;if(ql<=l&&r<=qr){apply(p,d);return;}push(p);int m=(l+r)/2;add(2*p,l,m,ql,qr,d);add(2*p+1,m,r,ql,qr,d);pull(p);}
 void low_ranges(std::int64_t target,std::vector<std::pair<int,int>>&out){collect(1,0,n,target,out);if(out.empty())return;std::vector<std::pair<int,int>>m;m.reserve(out.size());for(auto z:out){if(!m.empty()&&m.back().second==z.first)m.back().second=z.second;else m.push_back(z);}out.swap(m);}
 void collect(int p,int l,int r,std::int64_t target,std::vector<std::pair<int,int>>&out){if(mn[p]>=target)return;if(mx[p]<target){out.push_back({l,r});return;}if(r-l==1){out.push_back({l,r});return;}push(p);int m=(l+r)/2;collect(2*p,l,m,target,out);collect(2*p+1,m,r,target,out);}
};

Audit audit(const Sample&z,const std::vector<Atom>&atoms){
 Integer p=z.p,q=z.q,d=q*q+p*p,c=q*q-p*p,s=2*p*q,sum=c+s,dif=c-s;
 Integer tt=kSideNumerator*d-kSideDenominator*sum;if(tt<=0||c<=0||s<0||dif<=0)throw std::runtime_error("physical chamber");
 Integer extent=kGrid*tt*sum/2,cu=kGrid*kSideNumerator*d*sum/2,cv=kGrid*kSideNumerator*d*dif/2;
 Integer minu=cu-extent,maxu=cu+extent,minv=cv-extent,maxv=cv+extent,proj=kGrid*d*d*tt;
 std::vector<Rect>rs;rs.reserve(atoms.size());std::vector<Integer>xe{minu,maxu},ye{minv,maxv};xe.reserve(2*atoms.size()+2);ye.reserve(2*atoms.size()+2);
 for(auto a:atoms){Integer au=a.x*c+a.y*s,av=-a.x*s+a.y*c;Integer l=kSideDenominator*d*(au-(kGrid/2)*d),r=kSideDenominator*d*(au+(kGrid/2)*d),b=kSideDenominator*d*(av-(kGrid/2)*d),t=kSideDenominator*d*(av+(kGrid/2)*d);rs.push_back({l,r,b,t,a.w});if(minu<=l&&l<=maxu)xe.push_back(l);if(minu<=r&&r<=maxu)xe.push_back(r);if(minv<=b&&b<=maxv)ye.push_back(b);if(minv<=t&&t<=maxv)ye.push_back(t);}
 std::sort(xe.begin(),xe.end());xe.erase(std::unique(xe.begin(),xe.end()),xe.end());std::sort(ye.begin(),ye.end());ye.erase(std::unique(ye.begin(),ye.end()),ye.end());int nx=xe.size()-1,ny=ye.size()-1;
 auto clipidx=[](const Integer&x,const Integer&lo,const Integer&hi,const std::vector<Integer>&e,int n){if(x<=lo)return 0;if(x>=hi)return n;return exact_index(e,x);};
 std::vector<std::vector<Event>>ev(nx+1);
 for(auto r:rs){int l=clipidx(r.l,minu,maxu,xe,nx),rr=clipidx(r.r,minu,maxu,xe,nx),b=clipidx(r.b,minv,maxv,ye,ny),t=clipidx(r.t,minv,maxv,ye,ny);if(l>=rr||b>=t)continue;ev[l].push_back({b,t,r.w});ev[rr].push_back({b,t,-r.w});}
 SegTree st(ny);std::uint64_t runs=0;std::int64_t mincov=std::numeric_limits<std::int64_t>::max();std::vector<std::pair<int,int>>low;low.reserve(64);
 for(int i=0;i<nx;++i){for(auto e:ev[i])st.add(e.l,e.r,e.d);mincov=std::min(mincov,st.mn[1]);if(st.mn[1]>=kCoverageTarget)continue;low.clear();st.low_ranges(kCoverageTarget,low);for(auto [a,b]:low){++runs;if(intersects(xe[i],xe[i+1],ye[a],ye[b],cu,cv,extent,proj,c,s))return {false,runs,mincov};}}
 return {true,runs,mincov};
}
}

int main(int argc,char**argv){try{int threads=argc>1?std::stoi(argv[1]):8;std::string ap=argc>2?argv[2]:"atoms.csv",sp=argc>3?argv[3]:"samples.tsv";omp_set_num_threads(threads);auto atoms=load_atoms(ap);auto samples=load_samples(sp);int begin=argc>4?std::stoi(argv[4]):0;int end=argc>5?std::stoi(argv[5]):(int)samples.size();begin=std::max(0,begin);end=std::min((int)samples.size(),end);std::atomic<bool>ok(true);unsigned long long runs=0;long long gmin=std::numeric_limits<long long>::max();double start=omp_get_wtime();
 for(int i=begin;i<end;++i){if(!ok.load())continue;auto r=audit(samples[i],atoms);runs+=r.runs;gmin=std::min(gmin,(long long)r.mincov);if(!r.ok){ok=false;
std::cerr<<"failure cell="<<i<<"\n";}if((i-begin)%100==0){
std::cerr<<"progress="<<i<<" sec="<<(omp_get_wtime()-start)<<"\n";}}
 std::cout<<"cells="<<(end-begin)<<" runs="<<runs<<" min_arrangement_coverage="<<gmin<<" ok="<<ok.load()<<" seconds="<<(omp_get_wtime()-start)<<"\n";if(!ok.load())return 1;std::cout<<"EXACT SEGMENT COVERAGE PASS\n";return 0;
}catch(const std::exception&e){std::cerr<<"error: "<<e.what()<<"\n";return 2;}}
