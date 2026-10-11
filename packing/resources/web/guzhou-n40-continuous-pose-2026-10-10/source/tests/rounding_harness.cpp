// 冻结区间算术及环境守卫的回归。
// Regression of frozen interval rounding and environment guards.
#define main continuous_entry
#include "continuous_pose.cpp"
#undef main
#include <random>
int main(int argc,char**argv){
 if(argc>1){
  if(string(argv[1])=="rounding")fesetround(FE_DOWNWARD);
#if defined(__SSE__)
  if(string(argv[1])=="ftz")_mm_setcsr(_mm_getcsr()|(1u<<15));
#endif
  char a0[]="continuous",a1[]="1",a2[]="500",a3[]="1000000",a4[]="4999",a5[]="5000",a6[]="1";
  char* args[]={a0,a1,a2,a3,a4,a5,a6};return continuous_entry(7,args);
 }
 mt19937_64 rng(4010041010ULL);unsigned long long count=0;
 auto test=[&](double x){
  double u=up(x),d=dn(x),eu=nextafter(x,INFINITY),ed=nextafter(x,-INFINITY);
  assert((isnan(u)&&isnan(eu))||memcmp(&u,&eu,8)==0);
  assert((isnan(d)&&isnan(ed))||memcmp(&d,&ed,8)==0);++count;
 };
 for(double x:{0.,-0.,1.,-1.,double(INFINITY),-double(INFINITY),numeric_limits<double>::denorm_min(),numeric_limits<double>::max()})test(x);
 for(int j=0;j<1000000;j++){uint64_t bits=rng();double x;memcpy(&x,&bits,8);test(x);}
 cout<<"{\"status\":\"PASSED\",\"values\":"<<count<<",\"seed\":4010041010}"<<endl;
}
