pragma solidity ^0.8.19;
contract transcache {
    
    event Transfercachedcontent(string Content_key,string hash_ID, string token_sign, int256 splitsizecontent_ID);
    struct Content_cache {
        
        string hash_ID;
        string token_sign;
        int256 splitsizecontent_ID; 
    }
    
    mapping(string => mapping(uint256 =>Content_cache)) public Contentcache;
    string[] public ContentkeyArray;
    uint256 id=1;
    string Generalcontentkey;
    Content_cache restoreContentcache;
    constructor () {
       
        ContentkeyArray.push("0");
        Content_cache memory initContentcache=Content_cache({ hash_ID:"",token_sign:"",splitsizecontent_ID:0});
        Contentcache["0"][0]=initContentcache;
      
    }
        
    function Storecontentinedgeservercache(string memory Contentkey,string memory hashID, string memory  tokensign, int256 splitsizecontentID )public {
        Content_cache memory struct_Contentcache=Content_cache(hashID,tokensign,splitsizecontentID);
        Contentcache[Contentkey][id]=struct_Contentcache;
        ContentkeyArray.push(Contentkey);
        id++;
        emit Transfercachedcontent(Contentkey,struct_Contentcache.hash_ID,struct_Contentcache.token_sign,struct_Contentcache.splitsizecontent_ID);

    }
    
    function Readcontentfromedgeservercache(string memory Contentkey)public returns(Content_cache memory){
        string memory _Contentkey;
        Generalcontentkey=Contentkey;
        for(uint i=ContentkeyArray.length-1;i>0;i--)
        {
            _Contentkey=ContentkeyArray[i];
            if(keccak256(abi.encodePacked(_Contentkey)) == keccak256(abi.encodePacked(Contentkey)))
            {
                restoreContentcache=Contentcache[Contentkey][i];
                break;
            }
            else{
                restoreContentcache=Content_cache({ hash_ID:"",token_sign:"",splitsizecontent_ID:0});
            }
        }
        return restoreContentcache;

    }
    function getcontentfromedgeservercache()public view returns(Content_cache memory)
    {
        return restoreContentcache;
    }


        
}