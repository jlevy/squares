// SHA-256 of the actual input bytes, plus JSON-safe argument echo.
#pragma once
#include <sstream>
#include <iterator>
#include <stdexcept>
static uint32_t rotr(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static std::string sha256_file(const char* path){
 std::ifstream f(path,std::ios::binary);if(!f)throw std::runtime_error("hash input unavailable");
 std::vector<unsigned char> b((std::istreambuf_iterator<char>(f)),{});uint64_t bits=uint64_t(b.size())*8;
 b.push_back(128);while(b.size()%64!=56)b.push_back(0);for(int i=7;i>=0;--i)b.push_back((bits>>(8*i))&255);
 uint32_t h[]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
 const uint32_t k[]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
 for(size_t off=0;off<b.size();off+=64){uint32_t w[64];for(int i=0;i<16;i++)w[i]=(uint32_t(b[off+4*i])<<24)|(uint32_t(b[off+4*i+1])<<16)|(uint32_t(b[off+4*i+2])<<8)|b[off+4*i+3];
 for(int i=16;i<64;i++)w[i]=w[i-16]+(rotr(w[i-15],7)^rotr(w[i-15],18)^(w[i-15]>>3))+w[i-7]+(rotr(w[i-2],17)^rotr(w[i-2],19)^(w[i-2]>>10));
 uint32_t a=h[0],c=h[2],d=h[3],e=h[4],g=h[6],hh=h[7],bb=h[1],ff=h[5];
 for(int i=0;i<64;i++){uint32_t t1=hh+(rotr(e,6)^rotr(e,11)^rotr(e,25))+((e&ff)^(~e&g))+k[i]+w[i];uint32_t t2=(rotr(a,2)^rotr(a,13)^rotr(a,22))+((a&bb)^(a&c)^(bb&c));hh=g;g=ff;ff=e;e=d+t1;d=c;c=bb;bb=a;a=t1+t2;}
 h[0]+=a;h[1]+=bb;h[2]+=c;h[3]+=d;h[4]+=e;h[5]+=ff;h[6]+=g;h[7]+=hh;}
 const char* hex="0123456789abcdef";std::string out;for(auto x:h)for(int i=7;i>=0;i--)out+=hex[(x>>(4*i))&15];return out;
}
static std::string identity(int argc,char**argv,const char* input){
 std::ostringstream o;o<<"\"input_sha256\":\""<<sha256_file(input)<<"\",\"arguments\":[";
 for(int i=1;i<argc;i++){if(i>1)o<<',';o<<'"';for(unsigned char c:std::string(argv[i])){if(c=='"'||c=='\\')o<<'\\';if(c<32)throw std::runtime_error("control in argument");o<<c;}o<<'"';}o<<"],";return o.str();
}
