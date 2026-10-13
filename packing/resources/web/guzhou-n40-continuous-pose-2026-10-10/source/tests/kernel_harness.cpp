#define main pose_entry
#include "continuous_pose.cpp"
#undef main
int main(){
  cout<<setprecision(17);int cases;cin>>cases;
  for(int j=0;j<cases;j++){
    I L=readI(cin),B=readI(cin),T=readI(cin);Direction d=direction(T);set_frame(B,d);
    double u,v,du,dv;int nr;cin>>u>>v>>du>>dv>>nr;vector<R>rs;
    for(int k=0;k<nr;k++){R r;r.a=readI(cin);r.b=readI(cin);r.d=readI(cin);r.e=readI(cin);r.rho=readI(cin);rs.push_back(r);}
    Node n{u,v,du,dv,0,0,rs,.5,.5};auto cl=classify(n,L,B,d.c,d.s);auto b=bound(u,v,du,dv,L,B,d.c,d.s,cl.active);
    I E=L/I(2)-B*(d.c+d.s)/I(2),cx=L/I(2)+I(u)*E,cy=L/I(2)+I(v)*E;
    cout<<"{\"case\":"<<j<<",\"lower\":"<<dn(cl.base+b.lower)<<",\"center\":"<<dn(cl.base+b.center)<<",\"inside\":"<<cl.inside<<",\"outside\":"<<cl.outside<<",\"areas\":[";
    for(int k=0;k<nr;k++){if(k)cout<<",";cout<<area_lower(rs[k],cx,cy,d.c,d.s,B);}cout<<"]}"<<endl;
  }
}
