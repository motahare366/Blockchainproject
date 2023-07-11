// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.19;
import {SD59x18, sd} from "../prb-math-main/src/SD59x18.sol";

import {unwrap, wrap} from "../prb-math-main/src/sd59x18/Helpers.sol";
import {toSD59x18, fromSD59x18, convert} from "../prb-math-main/src/sd59x18/Conversions.sol";
import {sd59x18} from "../prb-math-main/src/sd59x18/Casting.sol";

contract Reputationcalculation  {
    struct edgeserver{
        bool exists;
        bool blacklist;
       // uint ID;
        //uint reputation;
    }
    mapping (address => edgeserver) public edgeserver_suppliers;
      struct mobileuser{
      bool exists;
      //uint ID;
    }
    //mapping(address => mapping(address => edgeserver)) public edgeserverID ;
    mapping (address => mobileuser) public mobileusers;
    mapping(address => mapping(address =>mapping (uint256=>int256))) public reputation;
    mapping(int256 => edgeserver) public listedgeservers;
    mapping(int256 =>mobileuser) public  listedmobileuser;
    address payable private owner; 
    address[] public mobileuserArray;
    address[] public edgeserverArray;
    int256[]public Eui;
    address[] public DRusimobileuser;
    address[] public DRusiedgeserver;
    address[] public duplicateuser;
    address[] public blacklistedgeserver;
    int256[] public result;
    SD59x18[]public resultDirection;
    int256[]public resultInDirection;

    uint256 id=1;
    int256 SDSub;//
    int256 SDSqr;//
    SD59x18 one=sd(1e18);
    //int256 IncrementSIC=0;
    int256 reputationSum=0 ;//
    int256  reputationAverage;//
    //SD59x18 SDdiv;
    //SD59x18 SDus;
    //SD59x18 SDusexp;
    SD59x18 REus; 
    SD59x18 resultf;
    SD59x18 DRus;
    uint256 DRusinumber=1;
    uint256 tinumber=1;
    int256 T=0;
    int256 n;
    //SD59x18 SICdiv;
    SD59x18 a;
    SD59x18 B;
    mapping(address => mapping(address =>mapping (uint256=>SD59x18))) public DRusi;
    mapping(address => mapping(address =>mapping (uint256=>int256))) public ti;
    mapping(address => mapping(uint256 => int256)) public Rusi;
    int256 Rus;
    ///
    //SD59x18 NRus;
    //SD59x18 DRis;
    //int256 tti;
    address _edgeserver;
    address _mobileuser;
    event TestDirection(SD59x18[]_resultDirection,SD59x18 _DRus);
    event TestInDirection(int256[]_resultInDirection,int256 _Rus);
    
    constructor () {
        owner =payable( msg.sender);
        edgeserverArray.push(0x0000000000000000000000000000000000000000);
        mobileuserArray.push(0x0000000000000000000000000000000000000000);
        reputation[0x0000000000000000000000000000000000000000][0x0000000000000000000000000000000000000000][0]= 0;
        DRusimobileuser.push(0x0000000000000000000000000000000000000000);
         DRusiedgeserver.push(0x0000000000000000000000000000000000000000);
        n=0;
    }
    function setaB(SD59x18 _a,SD59x18 _B)public returns(int256)
    {
       int256 sumaB=unwrap(_a)+unwrap(_B);
       require(sumaB==1000000000000000000,"The entered value is wrong, please enter it again.");
       a=_a;
       B=_B;
       return sumaB;
    }
    function DirectReputation( address edgeserver,address mobileuser,int256 Eus )public returns(int256) { 
        for(uint i=0;i<blacklistedgeserver.length;i++)
      {
        if(blacklistedgeserver[i]==edgeserver){
          require(edgeserver_suppliers[edgeserver].blacklist,"Edge server is blacklisted");

        }
      }
        require(0<=Eus && Eus<=1000000000000000000,"The entered value is wrong, please enter it again.");
        
        delete Eui;
        int256 t=0;
        int256 SIC=0;
        int256 numRatings =0;
        reputationSum=0;
        reputationAverage=0;
        SDSub=0;
        SDSqr=0;
        REus=sd(0e18);
        DRus=sd(0e18);
        resultf=sd(0e18);
        n=0;
//400000000000000000
    for(uint256 i=1;i<mobileuserArray.length;i++)
    {
        _edgeserver=edgeserverArray[i];
        _mobileuser=mobileuserArray[i];
        if(mobileuser==_mobileuser){
           Eui.push(reputation[_edgeserver][_mobileuser][i]);
           reputationSum += reputation[_edgeserver][_mobileuser][i];
           numRatings++;
           if(edgeserver==_edgeserver)
           {
              SIC++;
           }
          
       }
    }
   
    if(numRatings==0){
    edgeserverArray.push(edgeserver);
    mobileuserArray.push(mobileuser);
    reputation[edgeserver][mobileuser][id]= Eus;
     id++;
    }
    if(SIC==0){
       edgeserverArray.push(edgeserver);
       mobileuserArray.push(mobileuser);
       reputation[edgeserver][mobileuser][id]= Eus;
       id++;
    }
    if(SIC!=0){
       if(numRatings!=0){
        //SIC=SIC+1;
        //numRatings=numRatings+1;
        //reputationSum=reputationSum+Eus;
        reputationAverage=reputationSum / numRatings;
        for(uint i=0;i<Eui.length;i++)
      {
            SDSub=Eui[i]-reputationAverage;
            SDSqr+=SDSub**2;
     }
            // SDSqr=Eus-reputationAverage;
            // SDSub+=SDSqr**2;
    edgeserverArray.push(edgeserver);
    mobileuserArray.push(mobileuser);
    reputation[edgeserver][mobileuser][id]=Eus;
    id++;
    //SD59x18 int256SDSubintoSD59x18= SD59x18.wrap(SDSub);
   // SD59x18 int256numRatingsintoSD59x18= wrap(numRatings);
    //SD59x18 int256oneintoSD59x18= wrap(one);  
   SD59x18 SDdiv=(SD59x18.wrap( SDSqr)).div( wrap(numRatings));
    int256 SD59x18SDdivtoint256 =unwrap(SDdiv);
    SD59x18SDdivtoint256=SD59x18SDdivtoint256/1000000000000000000;
    SD59x18SDdivtoint256=SD59x18SDdivtoint256/1000000000000000000;
    SDdiv=wrap(SD59x18SDdivtoint256);
     SD59x18 SDus=SDdiv.sqrt();
     SD59x18 SDusexp=SDus.exp();
     REus=one.div(SDusexp);
     //int256 SIC1e18=SIC*1e18;
     //SIC1e18=SIC1e18*1e18;
     //SD59x18 int256SICintoSD59x18=SD59x18.wrap(SIC);
     //IncrementSIC=SIC+1;
     //SD59x18 int256IncrementSICintoSD59x18=wrap(SIC+1);
     SD59x18 SICdiv=(SD59x18.wrap(SIC)).div(wrap(SIC+1));
     SD59x18 f=SICdiv.sqrt();
     resultf=f;
     //SD59x18 EusSD59x18=wrap(Eus);
     DRus=f.mul(REus.mul(wrap(Eus)));
     DRusimobileuser.push(mobileuser);
     DRusiedgeserver.push(edgeserver);
     DRusi[edgeserver][mobileuser][DRusinumber]=DRus;
     ti[edgeserver][mobileuser][tinumber]=SIC;
     //result.push(SIC);
     DRusinumber++;
     tinumber++;
      for(uint j=0;j<mobileuserArray.length;j++)
     {
         _edgeserver=edgeserverArray[j];
        _mobileuser=mobileuserArray[j];
        if(edgeserver==_edgeserver){
           t++;
          duplicateuser.push(mobileuserArray[j]);
           
       }
     }
     int256 duplicatN=0;
     uint count=duplicateuser.length;
     uint j=0;
     address[] memory remove = new address[](count);
     for( uint i=0;i<count-1;i++){
     if(duplicateuser[i]!=duplicateuser[i+1]){
        remove[j++]=duplicateuser[i];
      }
     }
    remove[j++]=duplicateuser[count-1];
    for(uint i=0;i<count;i++)
    {
       if(remove[i]!=0x0000000000000000000000000000000000000000)
       {
          duplicatN++;
       }
    }
       T=t;
       n=duplicatN;
    }

    }
    
    resultDirection=[REus,DRus,resultf,wrap(t),wrap(T),wrap(SIC),wrap(n)];
      assert(0<=unwrap(DRus) && unwrap(DRus)<=1000000000000000000);

      emit TestDirection(resultDirection,DRus) ;  
      return SDSqr; 
   }
   function IndirectReputation( address edgeserver,address mobileuser)public  {
   
     for(uint i=0;i<blacklistedgeserver.length;i++)
      {
        if(blacklistedgeserver[i]==edgeserver){
          require(!edgeserver_suppliers[edgeserver].blacklist,"Edge server is blacklisted");

        }
      }
     
     SD59x18 Tti;
     SD59x18 sumDRti;
     SD59x18 NRus;
     if(DRusimobileuser.length==1){
        Rus=300000000000000000;
     }
     if(DRusimobileuser.length!=1)
     {
         for(uint256 i=DRusimobileuser.length-1;i>0;i--)
         {
            address _edgeserver=DRusiedgeserver[i];
            address _mobileuser=DRusimobileuser[i];
            if(edgeserver==_edgeserver){
            int256 tti=ti[edgeserver][mobileuser][i];
            //gg=tti;
            int256 subti=T-tti;
             result.push(subti);
            SD59x18 int256subtiintoSD59x18= SD59x18.wrap(subti);
            SD59x18 subtiexp=int256subtiintoSD59x18.exp();
            
            Tti=one.div(subtiexp);
            SD59x18 DRis=DRusi[edgeserver][mobileuser][i];
              SD59x18 mulRti =Tti.mul(DRis);
              sumDRti =sumDRti.add(mulRti);
              break;
            }
         }
      }
      if(n==0){
       Rus=300000000000000000;
      }
      if(n!=0){
       SD59x18 int256nintoSD59x18= wrap(n);

       NRus=sumDRti.div(int256nintoSD59x18);
       assert(0<=(unwrap(NRus)/1000000000000000000) && (unwrap(NRus)/1000000000000000000)<=1000000000000000000);
       SD59x18 mulRus1=a.mul(DRus);
       SD59x18 mulRus2=B.mul(NRus);
       int256 Rus1=unwrap(mulRus1);
       int256 Rus2=unwrap(mulRus2)/1000000000000000000;
       //SD59x18 sumRus=Rus1.add(Rus2);
       Rus=Rus1 + Rus2;
      }
       uint256 Rusnumber=1;
       Rusi[edgeserver][Rusnumber]=Rus;
       Rusnumber++;
       if(Rus<=0){
       blacklistedgeserver.push(edgeserver);
       edgeserver_suppliers[edgeserver].blacklist=true;
       }
    resultInDirection=[(unwrap(NRus)/1000000000000000000),Rus];
    assert(0<=Rus && Rus<=1000000000000000000);
    emit TestInDirection(resultInDirection,Rus);
    

   }
   
   function ReputationofEdgeServers(address edgeserver)public returns(int256){
    address _edgeserver;
    int256 reputationedgeserver ;
    for(uint i=DRusiedgeserver.length-1;i>0;i--){
        _edgeserver=DRusiedgeserver[i];
        if(_edgeserver==edgeserver){
           reputationedgeserver=Rusi[edgeserver][i];
         }
       break; 
    }
    return reputationedgeserver;
  }
  
  function getid() public view returns(uint256 ) {
    
     return id;
  }
   function getRus() public view returns(int256 ) {
    
      return Rus;
   }
  function getn() public view returns(int256 ) {
    
     return n;
  }
  function getREus() public view returns(SD59x18 ) {
    
     return REus;
  }
  function getDRus() public view returns(SD59x18 ) {
    
     return DRus;
  }
  
  function getresultDirection() public view returns(SD59x18[]memory ) {
    
     return resultDirection;
  }
  function getresultInDirection() public view returns(int256[]memory ) {
    
     return resultInDirection;
  }
  
  

}