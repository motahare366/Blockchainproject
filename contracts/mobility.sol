// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.19;
contract storepublickkey {
    
    event storepublickeysmobileuser(address mobileuser,string public_keymu,int256 Rus );
    struct Public_key{
        string public_keymu;
        int256 Rus;
        
    }
    
    mapping(address => mapping(uint256 =>Public_key)) public key;
    address public mobileuser;
    address[] public mobileuserArray;
    uint256 id=1;
    bool exists;
    Public_key restorepublickey;
    uint256 l;
    constructor () {
       
         mobileuserArray.push(0x0000000000000000000000000000000000000000);
        Public_key memory initpublickey=Public_key({ public_keymu:"", Rus:300000000000000000});
         key[0x0000000000000000000000000000000000000000][0]=initpublickey;
        exists=false;
    }
        
    function storeintheblockchain(address mobile,string memory pknmu,int256 _Rus )public {
       
        
        Public_key memory publickey =Public_key(pknmu,_Rus);
        
        key[mobile][id]=publickey;
        mobileuserArray.push(mobile);
        
        id++;
        l=mobileuserArray.length;
        emit storepublickeysmobileuser(mobileuser,publickey.public_keymu,publickey.Rus);
    
    }
    
     
     function Researchpublickey(address mobile)public returns(Public_key memory ){

        exists=false;
        address _mobile;
        mobileuser=mobile;
      
       for(uint i=mobileuserArray.length-1;i>0;i--)
       {
          
           _mobile=mobileuserArray[i];
            if(_mobile==mobile){
               restorepublickey=key[mobile][i];
               exists=true;
                
               break; 
            }
            else{
              exists=false;
              restorepublickey=Public_key({ public_keymu:"", Rus:200000000000000000});
            }
        
             
       }
       
      return  restorepublickey;
    
      
    }
    function Existingpublickey()public view returns(bool){
      
      return exists;
    }
    function getResearchpublickey()public view returns(Public_key memory){
        return restorepublickey;
    }
    function getlengh() public view returns(uint256){
        return l;
    }

   


}
