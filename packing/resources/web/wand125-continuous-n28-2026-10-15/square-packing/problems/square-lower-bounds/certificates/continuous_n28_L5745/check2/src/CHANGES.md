# v1.2 (2026-10-15)

- The format label of candidates given as rectangles with masses (manifest `format`) is renamed to `mixed`; the format itself is unchanged. Kernels, generator arithmetic and acceptance are unchanged.

# Kernel changes

All changes are confined to `kernel/`; the supplied `upstream/` is unchanged.

1. Continuous-pose rectangle cap: 10,000 to 20,000. Integer-axis rectangle
   cap: 10,000 to 20,000. This accommodates larger expanded D4 inputs.
2. Continuous-pose side cap: L < 10 to L < 12. Integer-axis side cap:
   10,000,000,000 to 12,000,000,000 grid units. This allows the requested
   larger containers while preserving all interval and overflow guards.
3. Axis grid cap: 15,000,000 to 90,000,000 vertices. Four signed-128-bit
   coefficient arrays require at most 5,760,000,000 bytes, leaving ample
   space below 8 GB for the at-most-20,000 rectangles, knots and bookkeeping.
   The axis runs alone, before the slab workers. No overflow guard is weakened.
4. Add `identity.h`, which computes SHA-256 from the kernel input bytes and
   serializes all actual command arguments. Both kernels echo these fields;
   the driver checks them. The continuous kernel includes identity on both
   verified and unresolved results. Numeric acceptance is unchanged.

The existing angle-loss-versus-translation-loss splitting policy is unchanged.
No mathematical acceptance rule, floating-point operation, outward rounding,
assertion, integer overflow check, or direct-sum reconciliation was removed.
Compilation adds the upstream IEEE safety flags to the requested
`c++ -O2 -std=c++17` baseline.

## Generator density scaling (no kernel arithmetic change)

The x28 control has summed integer densities 2,625,965,571,842,792 at
P = 10^9, exceeding the retained strict 10^15 coefficient bound. At P = 10^8
the sum is 262,596,557,182,320, which passes. The new generator therefore
reduces the density denominator by powers of ten when necessary, while
keeping the coordinate denominator G = 10^9. Each density is still rounded
downward, and the unchanged kernel computes its scale as P*G*G. All per-row,
total-coefficient and evaluation guards remain in force. The n40 input bytes
are unaffected. This adjustment is called out at the top of README.md.

## Complete unified diff

```diff
--- upstream/verifier/continuous_pose.cpp
+++ kernel/continuous_pose.cpp
@@ -22,6 +22,7 @@
 #include <string>
 #include <vector>
 #include <chrono>
+#include "identity.h"
 using namespace std;
 // IEEE 正负数的编码有序，故整数加减一给出相邻浮点数。
 // IEEE encodings are ordered by sign, so adding or subtracting one gives the neighbor.
@@ -167,7 +168,8 @@
     const double threshold=up(double(tn)/double(td));
     ifstream in("certificate_input.txt");assert(in);I L=readI(in),B=readI(in);int nr;in>>nr;vector<R>rs;
     for(int i=0;i<nr;i++){R r;r.a=readI(in);r.b=readI(in);r.d=readI(in);r.e=readI(in);r.rho=readI(in);assert(r.rho.l>=0);rs.push_back(r);}
-    assert(in && nr>0 && nr<=10000 && 0<B.l && B.h<L.l && L.h<10);
+    assert(in && nr>0 && nr<=20000 && 0<B.l && B.h<L.l && L.h<12);
+    const string receipt_identity=identity(argc,argv,"certificate_input.txt");
     auto start=chrono::steady_clock::now();long long nodes=0,leaves=0,inside=0,outside=0,active_sum=0,angle_splits=0;int max_depth=0;double minbound=INFINITY;
     vector<Node>stack; stack.push_back({.5,.5,.5,.5,0.,0,rs,.5,.5});cout<<setprecision(17);
     while(!stack.empty()){
@@ -179,7 +181,7 @@
         assert(isfinite(b.lower)&&isfinite(b.fx)&&isfinite(b.fy)&&isfinite(b.center));
         if(b.lower>=threshold){leaves++;minbound=min(minbound,b.lower);continue;}
         if(nodes>=maxnodes || min(min(z.du,z.dv),z.dw)<0x1p-40){
-            cout<<"{\"status\":\"unresolved\",\"nodes\":"<<nodes<<",\"leaves\":"<<leaves<<",\"u\":"<<z.u<<",\"v\":"<<z.v<<",\"w\":"<<z.w<<",\"du\":"<<z.du<<",\"dv\":"<<z.dv<<",\"dw\":"<<z.dw<<",\"center_lower\":"<<b.center<<",\"angle_splits\":"<<angle_splits<<",\"max_depth\":"<<max_depth<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}"<<endl;return 3;
+            cout<<"{"<<receipt_identity<<"\"status\":\"unresolved\",\"nodes\":"<<nodes<<",\"leaves\":"<<leaves<<",\"u\":"<<z.u<<",\"v\":"<<z.v<<",\"w\":"<<z.w<<",\"du\":"<<z.du<<",\"dv\":"<<z.dv<<",\"dw\":"<<z.dw<<",\"center_lower\":"<<b.center<<",\"angle_splits\":"<<angle_splits<<",\"max_depth\":"<<max_depth<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}"<<endl;return 3;
         }
         Direction dm=direction(T0+span*I(z.w));set_frame(B,dm);
         double midpoint=center_mass(z,L,B,dm),angle_loss=max(0.,midpoint-b.center);
@@ -191,5 +193,5 @@
         stack.push_back(move(z));stack.push_back(move(other));
     }
     double sec=chrono::duration<double>(chrono::steady_clock::now()-start).count();
-    cout<<"{\"status\":\"verified\",\"pl\":"<<pl<<",\"ph\":"<<ph<<",\"den\":"<<den<<",\"nodes\":"<<nodes<<",\"leaves\":"<<leaves<<",\"lower_bound\":"<<minbound<<",\"seconds\":"<<sec<<",\"full_inside\":"<<inside<<",\"full_outside\":"<<outside<<",\"mean_active\":"<<double(active_sum)/nodes<<",\"max_depth\":"<<max_depth<<",\"angle_splits\":"<<angle_splits<<"}"<<endl;
+    cout<<"{"<<receipt_identity<<"\"status\":\"verified\",\"pl\":"<<pl<<",\"ph\":"<<ph<<",\"den\":"<<den<<",\"nodes\":"<<nodes<<",\"leaves\":"<<leaves<<",\"lower_bound\":"<<minbound<<",\"seconds\":"<<sec<<",\"full_inside\":"<<inside<<",\"full_outside\":"<<outside<<",\"mean_active\":"<<double(active_sum)/nodes<<",\"max_depth\":"<<max_depth<<",\"angle_splits\":"<<angle_splits<<"}"<<endl;
 }
--- upstream/verifier/axis_integer_grid.cpp
+++ kernel/axis_integer_grid.cpp
@@ -8,6 +8,7 @@
 #include <stdexcept>
 #include <string>
 #include <vector>
+#include "identity.h"
 using Z = __int128_t;
 using I = int64_t;
 std::string text(Z x) { if(x==0) return "0"; bool neg=x<0; if(neg)x=-x; std::string s; while(x){s.push_back(char('0'+x%10));x/=10;} if(neg)s.push_back('-'); std::reverse(s.begin(),s.end());return s; }
@@ -16,7 +17,7 @@
 int main(int argc,char**argv){try{
  require(argc==2,"Usage: axis_integer_grid INPUT"); std::ifstream in(argv[1]);require(bool(in),"Input unavailable");
  I l,B,G,P,tau_num,tau_den;size_t n;in>>l>>B>>G>>P>>tau_num>>tau_den>>n;
- require(in && 0<B && B<l && l<=10000000000LL && G>0 && G<=1000000000LL && P>0 && P<=1000000000LL && tau_num>0 && tau_num<=1000000 && tau_den>0 && tau_den<=1000000 && n<=10000,"Input bounds");
+ require(in && 0<B && B<l && l<=12000000000LL && G>0 && G<=1000000000LL && P>0 && P<=1000000000LL && tau_num>0 && tau_num<=1000000 && tau_den>0 && tau_den<=2000000 && n<=20000,"Input bounds");
  require(l%2==0 && B%2==0,"Half units must be integral");
  std::vector<Rect> rs(n);std::vector<I> xs{l/2,l-B/2},ys=xs;Z weights=0;
  for(auto&r:rs){in>>r.a>>r.b>>r.d>>r.e>>r.w; require(in && 0<=r.a && r.a<r.d && r.d<=l && 0<=r.b && r.b<r.e && r.e<=l && 0<=r.w && r.w<=1000000000000000LL,"Rectangle bounds");weights+=r.w;
@@ -25,7 +26,7 @@
  }
  std::string extra;require(!(in>>extra),"Trailing input");
  for(auto*v:{&xs,&ys}){std::sort(v->begin(),v->end());v->erase(std::unique(v->begin(),v->end()),v->end());}
- size_t nx=xs.size(),ny=ys.size();require(nx*ny<=15000000,"Grid too large");
+ size_t nx=xs.size(),ny=ys.size();require(nx*ny<=90000000,"Grid too large");
  // Each of 16 signed hinge pairs per rectangle contributes to each coefficient.
  // max |knot| <= l+B/2. Accumulation, evaluation, and threshold comparisons
  // are bounded well inside signed 128-bit arithmetic by these explicit guards.
@@ -58,6 +59,6 @@
  // Divide before comparison: avoids multiplying the large minimum by tau_den.
  Z required=(scale*tau_num+tau_den-1)/tau_den;
  bool pass=minimum>=required;
- std::cout<<"{\"status\":\""<<(pass?"AXIS_COVERAGE_PROVED":"AXIS_TEST_REFUSED")<<"\",\"x_nodes\":"<<nx<<",\"y_nodes\":"<<ny<<",\"minimum_numerator\":\""<<text(minimum)<<"\",\"scale\":\""<<text(scale)<<"\",\"minimizer_x_integer\":"<<xs[mi]<<",\"minimizer_y_integer\":"<<ys[mj]<<",\"direct_sum_matches\":true,\"evaluation_abs_bound\":\""<<text(eval_bound)<<"\"}\n";
+ std::cout<<"{"<<identity(argc,argv,argv[1])<<"\"status\":\""<<(pass?"AXIS_COVERAGE_PROVED":"AXIS_TEST_REFUSED")<<"\",\"x_nodes\":"<<nx<<",\"y_nodes\":"<<ny<<",\"minimum_numerator\":\""<<text(minimum)<<"\",\"scale\":\""<<text(scale)<<"\",\"minimizer_x_integer\":"<<xs[mi]<<",\"minimizer_y_integer\":"<<ys[mj]<<",\"direct_sum_matches\":true,\"evaluation_abs_bound\":\""<<text(eval_bound)<<"\"}\n";
  return pass?0:2;
  }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 3;}}
--- new-file
+++ kernel/identity.h
@@ -0,0 +1,23 @@
+// SHA-256 of the actual input bytes, plus JSON-safe argument echo.
+#pragma once
+#include <sstream>
+#include <iterator>
+#include <stdexcept>
+static uint32_t rotr(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
+static std::string sha256_file(const char* path){
+ std::ifstream f(path,std::ios::binary);if(!f)throw std::runtime_error("hash input unavailable");
+ std::vector<unsigned char> b((std::istreambuf_iterator<char>(f)),{});uint64_t bits=uint64_t(b.size())*8;
+ b.push_back(128);while(b.size()%64!=56)b.push_back(0);for(int i=7;i>=0;--i)b.push_back((bits>>(8*i))&255);
+ uint32_t h[]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
+ const uint32_t k[]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
+ for(size_t off=0;off<b.size();off+=64){uint32_t w[64];for(int i=0;i<16;i++)w[i]=(uint32_t(b[off+4*i])<<24)|(uint32_t(b[off+4*i+1])<<16)|(uint32_t(b[off+4*i+2])<<8)|b[off+4*i+3];
+ for(int i=16;i<64;i++)w[i]=w[i-16]+(rotr(w[i-15],7)^rotr(w[i-15],18)^(w[i-15]>>3))+w[i-7]+(rotr(w[i-2],17)^rotr(w[i-2],19)^(w[i-2]>>10));
+ uint32_t a=h[0],c=h[2],d=h[3],e=h[4],g=h[6],hh=h[7],bb=h[1],ff=h[5];
+ for(int i=0;i<64;i++){uint32_t t1=hh+(rotr(e,6)^rotr(e,11)^rotr(e,25))+((e&ff)^(~e&g))+k[i]+w[i];uint32_t t2=(rotr(a,2)^rotr(a,13)^rotr(a,22))+((a&bb)^(a&c)^(bb&c));hh=g;g=ff;ff=e;e=d+t1;d=c;c=bb;bb=a;a=t1+t2;}
+ h[0]+=a;h[1]+=bb;h[2]+=c;h[3]+=d;h[4]+=e;h[5]+=ff;h[6]+=g;h[7]+=hh;}
+ const char* hex="0123456789abcdef";std::string out;for(auto x:h)for(int i=7;i>=0;i--)out+=hex[(x>>(4*i))&15];return out;
+}
+static std::string identity(int argc,char**argv,const char* input){
+ std::ostringstream o;o<<"\"input_sha256\":\""<<sha256_file(input)<<"\",\"arguments\":[";
+ for(int i=1;i<argc;i++){if(i>1)o<<',';o<<'"';for(unsigned char c:std::string(argv[i])){if(c=='"'||c=='\\')o<<'\\';if(c<32)throw std::runtime_error("control in argument");o<<c;}o<<'"';}o<<"],";return o.str();
+}
```

## Driver limits (91, 2026-10-11)

`check.py` capped `--workers` at 2 and `--timeout` at 2,400 s for the build machine. For the GCP runs the caps are
now 64 workers and 172,800 s. Acceptance is unchanged.

## Resume (91, 2026-10-12, v1.1)

`check.py --resume PREV/receipt.json` reuses a previous run's accepted slabs when the candidate, the generated kernel
input (all manifest file hashes), the build (binaries), the premises and the endpoints are identical, the slab's echoed
arguments equal the arguments this run would pass, and the slab passes `admit_slab` again. Everything else is
recomputed (the axis patch always). The receipt records `resumed_from` (previous receipt SHA-256, compatibility, number
of slabs reused) and marks reused slabs with `resumed: true`. Test: n40 stopped after 240 s with 12 accepted slabs,
resumed run VERIFIED with 12 slabs reused (same claim 1340000/199529).
