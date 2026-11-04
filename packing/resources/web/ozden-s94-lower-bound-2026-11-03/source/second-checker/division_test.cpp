#define main verifier_main
#include "intcheck_final.cpp"
#undef main
#include <random>
int main(){std::mt19937_64 gen(2039144);S=I(1)<<42;long n=0;for(int r=0;r<600;r++){C=120000LL*120000-r*(I)r*83*83;T=2LL*r*83*120000;D=120000LL*120000+r*(I)r*83*83;setup();for(int k=0;k<200;k++){W a=(W(gen()&((I(1)<<18)-1))<<64)|gen();if(k&1)a=-a;for(I b:{C,T,D,S,2*S}){if(!b)continue;W q=a/b,rem=a%b;if(rem<0)--q;assert(q==fd(a,b));n++;}}}printf("%ld exact signed floor divisions matched direct int128 division\n",n);return 0;}
