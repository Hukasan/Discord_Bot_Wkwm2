from hashids import Hashids
from random import randint


class MyHash:

    __hashids = Hashids(
        salt="test", alphabet="A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,0,1,2,3,4,5,6,7,8,9,{,},[,],(,),-,+,/,',|,^,*,_,$,&,#,!,?,;,`,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z")

    def gen(self) -> str:
        return self.__hashids.encode(randint(1, 5316911983139663491615228241121378304))

    def decode(self) -> int:
        return self.__hashids.decode(id)[0]
