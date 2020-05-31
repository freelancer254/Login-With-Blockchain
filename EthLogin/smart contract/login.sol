pragma solidity 0.6.1;
pragma experimental ABIEncoderV2;

//still needs gas limit for functions
//better looping mechanism

contract KenCertContract{
    address private owner;
    address [] private allowed_accounts;
    
    modifier onlyOwner(){
        if(owner==msg.sender){
            _;
        }
        else{
            revert();
        }
    }
    
    //I will add events 
    event allowAddressEvent(address indexed sender, address blocked );
    event blockAddressEvent(address indexed sender, address unblocked );
    
    //add account to the allowed_accounts array
    function allowAddress(address [] memory addressToAllow) onlyOwner public {
        for(uint k = 0; k < addressToAllow.length; k++){
            bool found = false;
            for(uint i=0; i<allowed_accounts.length;i++){
                if(allowed_accounts[i]==addressToAllow[k]){
                    found = true;
                    break;
                
                }
            }
            if(!found){
                allowed_accounts.push(addressToAllow[k]);
                emit allowAddressEvent(msg.sender, addressToAllow[k]);
            }
        }
        
    }
    
    //remove an account from the allowed_accounts array
    function blockAddress(address [] memory addressToBlock) onlyOwner public {
        for(uint k = 0; k < addressToBlock.length; k++){
            bool found = false;
            uint i;
            for(i=0; i<allowed_accounts.length;i++){
                if(allowed_accounts[i]==addressToBlock[k]){
                    found = true;
                    break;
                
                }
            }
            if(found){
                allowed_accounts[i] = allowed_accounts[allowed_accounts.length - 1];
                allowed_accounts.pop();
                emit blockAddressEvent(msg.sender, addressToBlock[k]);
            }
        }
    }
    
    //check whether an account is in the allowed_accounts array
    function checkBlockStatus(address addressToCheck) public view returns (bool ){
        bool blocked = true;
        for(uint i=0; i<allowed_accounts.length;i++){
            if(allowed_accounts[i]==addressToCheck){
                blocked  = false;
                break;
                
            }
        }
        return blocked;
    }
  

    //constructor and set the owner of the contract and allow the owner too
    constructor(address contractOwner) public {
        owner = contractOwner;
        allowed_accounts.push(contractOwner);
    }
    
}
