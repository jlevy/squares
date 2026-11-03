#define main verifier_main
#include "intcheck_final.cpp"
#undef main
int main(){long long c,t,d,x,X,y,Y,a,b;S=I(1)<<42;while(scanf("%lld%lld%lld%lld%lld%lld%lld%lld%lld",&c,&t,&d,&x,&X,&y,&Y,&a,&b)==9){C=c;T=t;D=d;setup();auto v=vertical(x,y,Y,a,b);auto h=horizontal(y,x,X,a,b);printf("%lld %lld %lld %lld %lld\n",(long long)area(x,X,y,Y,a,b),(long long)v.l,(long long)v.h,(long long)h.l,(long long)h.h);}return 0;}
