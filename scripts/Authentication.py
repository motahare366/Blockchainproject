from Crypto.PublicKey import RSA
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Cipher import PKCS1_OAEP
import binascii
import random
import json
import hashlib, secrets, binascii
from tinyec import registry
from scripts.encryption import encrypt_ECC ,decrypt_ECC  
import re 
from brownie import storepublickkey, config, network
#from scripts.helpful_scripts import get_account
import matplotlib.pyplot as plt
import math
from brownie import storepublickkey , accounts 
from brownie import Reputationcalculation, config, network
Nodekeys = {}
Serverkeys= {}
ticket= {}
hash_ticket={}
hash_r={}
Authenticationserverkeys={}
M1={}
M1_hash={}
###############
ContentID={}
index_ContentID={}
dict_byte_list_caching_token={}
dict_byte_list_caching_token_hash={}
#caching_token={}
############################
Authenticationserver="0x0000000000000000000000000000000000000000"
TS=0
account = accounts[0]
mobilityuser = storepublickkey.deploy({"from": account})
reputation = Reputationcalculation.deploy({"from": account})
def setMuconectedtoRc(mobileuseraddress):
    key_pairmu = RSA.generate(1024)
    public_keymu = key_pairmu.publickey().exportKey()
    private_keymu = key_pairmu.exportKey()
    key_listNodeRc = [public_keymu,private_keymu]
    Nodekeys[mobileuseraddress]=key_listNodeRc
def setMsconectedtoRc(edgeserveraddress):
   
          curve = registry.get_curve('brainpoolP256r1')
          private_keymsi = secrets.randbelow(curve.field.n)
          public_keymsi =  private_keymsi * curve.g
          key_listserverRc = [public_keymsi,private_keymsi]
          Serverkeys[edgeserveraddress]=key_listserverRc
          
#Generating keys for mobile users
def MuconectedtoRc(mobileuseraddress):
    dict_Nodekeys = list(Nodekeys)
    print(dict_Nodekeys)
    search_item = mobileuseraddress
    found = False

    
    if search_item in dict_Nodekeys:
      found=True
    else:
          key_pairmu = RSA.generate(1024)
          public_keymu = key_pairmu.publickey().exportKey()
          private_keymu = key_pairmu.exportKey()
          key_listNodeRc = [public_keymu,private_keymu]
          Nodekeys[mobileuseraddress]=key_listNodeRc
         #  print(key_listNodeRc[0])
         #  print(key_listNodeRc[1])
#Generating mobile server keys
def MsconectedtoRc(edgeserveraddress):
     
    dict_Serverkeys = list(Serverkeys)
    print(dict_Serverkeys)
    search_item =edgeserveraddress
    found = False

    
    if search_item in dict_Serverkeys:
           found = True
       
       
    else:
          curve = registry.get_curve('brainpoolP256r1')
          private_keymsi = secrets.randbelow(curve.field.n)
          public_keymsi =  private_keymsi * curve.g
          key_listserverRc = [public_keymsi,private_keymsi]
          Serverkeys[edgeserveraddress]=key_listserverRc
          #print(public_keymsi )
          #print(private_keymsi)
#Generation of authentication server keys
def GenerationAskeys():
    
    key_pairAs = RSA.generate(1024)
    public_keyAs = key_pairAs.publickey().exportKey()
    private_keyAs = key_pairAs.exportKey()
    key_listAs=[public_keyAs,private_keyAs]
    Authenticationserverkeys[Authenticationserver]=key_listAs
    #print(Authenticationserverkeys["0x0000000000000000000000000000000000000000"])
def MuconectedtoNewMs1(mobileuseraddress,edgeserveraddress):
  
   for key in Nodekeys.keys():
       if key==mobileuseraddress :
          key_listAs= Nodekeys[key]
          private_keymu=key_listAs[1]
   #print(private_keymu)
   
   #mobileuseraddress=mobileuseraddress.encode()
   TS_str=str(TS)
   M1_list=[mobileuseraddress,TS]
   M1_list_str=str(M1_list)
   byte_M1_list=M1_list_str.encode()
   hash = SHA256.new(byte_M1_list)
   keyPair= RSA.importKey(private_keymu)
   signer = PKCS115_SigScheme(keyPair)
   signature = signer.sign(hash)
   #print(len(signature))
   #print("Signature:", binascii.hexlify(signature))
   
   M1[mobileuseraddress,edgeserveraddress]=byte_M1_list
   M1_hash[mobileuseraddress,edgeserveraddress]=signature
   #print("m1",M1[mobileuseraddress])
def MuconectedtoNewMs2(mobileuseraddress,edgeserveraddress):
    Readfromblockchain=mobilityuser.Researchpublickey(mobileuseraddress,{"from": account})
    Authentication=mobilityuser.Existingpublickey({"from": account})
    if(Authentication==True):
       Searchkey_pkn=mobilityuser.getResearchpublickey()
       public_keymu=Searchkey_pkn[0].encode()
       #print("public_keymu",public_keymu)
   
       pubKeyObj =  RSA.importKey(public_keymu)
       for key in M1.keys():
          if mobileuseraddress in key :
             if edgeserveraddress in key:
                IDTS=M1[key]
       for key in M1_hash.keys():
          if mobileuseraddress in key :
             if edgeserveraddress in key:
                signature=M1_hash[key]
          
       hash = SHA256.new(IDTS)
       verifier = PKCS115_SigScheme(pubKeyObj)
      
       try:
             verifier.verify(hash, signature)
             print("Signature is valid.")
             print(TS)
             #TS=TS+1
             Eus = float(input('Enter Evaluation End user: '))
             Eus=Eus*100000000000000000
             
             Calculationofdirecttrust=reputation.DirectReputation(edgeserveraddress,mobileuseraddress,Eus,{"from": account})
             print( Calculationofdirecttrust.events)
             Calculationofindirecttrust=reputation.IndirectReputation(edgeserveraddress,mobileuseraddress,{"from": account})
             print(Calculationofindirecttrust.events)
             Rus=reputation.getRus({"from": account})
             print(Rus)

             
             wirteintoblockchain=mobilityuser.storeintheblockchain(mobileuseraddress,public_keymu,Rus,{"from": account})
             print(wirteintoblockchain.events)
             
            
            

       except:
               print("Signature is invalid.")
      #  #######!!!!!!!!!
    else:
        print("Connect to the authentication server")
        r=MuconectedtoAs1(mobileuseraddress,edgeserveraddress)
        pkas_rprime =MuconectedtoAs2(mobileuseraddress)
        ticket=MuconectedtoAs3(r,pkas_rprime,mobileuseraddress,edgeserveraddress)
        MuconectedtoMs1(mobileuseraddress,edgeserveraddress,ticket)
        

## AS to mu first stage
def MuconectedtoAs1(mobileuseraddress,edgeserveraddress):
    
    r=random.random()
    r= str(r)
    r=r.encode()
    for key in Nodekeys.keys():
       if key==mobileuseraddress :
          key_listAs= Nodekeys[key]
          public_keymu=key_listAs[0]
          private_keymu=key_listAs[1]
    
    keyEnmu = RSA.importKey(public_keymu)
    cipherEnmu = PKCS1_OAEP.new(keyEnmu)
    ciphertextr = cipherEnmu.encrypt( r)
    hash_r[ mobileuseraddress]=ciphertextr
    #print(r)
    #print(ciphertextr)
    return r
# AS to mu second stage
def MuconectedtoAs2(mobileuseraddress):
    for key in hash_r.keys():
       if key==mobileuseraddress :
          hashr_mu=hash_r[key]
          #print(hashr_mu) 
    for key in Nodekeys.keys():
       if key==mobileuseraddress :
          key_listAs= Nodekeys[key]
          private_keymu=key_listAs[1]
    keyDemu = RSA.importKey(private_keymu)
    cipherDemu = PKCS1_OAEP.new(keyDemu)
    rprime = cipherDemu.decrypt(hashr_mu)
    for key in Authenticationserverkeys.keys():
       if key==Authenticationserver :
          key_listAs= Authenticationserverkeys[key]
          public_keyAs=key_listAs[0]
    keyEnAs = RSA.importKey(public_keyAs)
    cipherEnAs = PKCS1_OAEP.new(keyEnAs)
    pkas_rprime= cipherEnAs.encrypt(rprime)
    #print(rprime)
    #print(pkas_rprime)
    return pkas_rprime 

# AS to mu third stage
def MuconectedtoAs3(r,pkas_rprime,mobileuseraddress,edgeserveraddress):
    for key in Authenticationserverkeys.keys():
       if key==Authenticationserver :
          key_listAs= Authenticationserverkeys[key]
          private_keyAs=key_listAs[1]
    keyDeAs = RSA.importKey(private_keyAs)
    cipherDeAs = PKCS1_OAEP.new(keyDeAs)
    rprime = cipherDeAs.decrypt(pkas_rprime)
    if r==rprime :
       print("Authentication is done")
       for key in Nodekeys.keys():
           if key==mobileuseraddress :
              key_listAs= Nodekeys[key]
              public_keymu=key_listAs[0]
       
       for key in Serverkeys.keys():
           if key==edgeserveraddress :# msi=gmi
               key_listservergmi= Serverkeys[key]
               public_keygmi=key_listservergmi[0]
              # print(public_keygmi)
       public_keygmibyte=str(public_keygmi)
       public_keygmibyte=public_keygmibyte.encode()
       listticket=[public_keymu,public_keygmibyte]
       byte_listticket=b''.join(listticket)
       print("################")    
       encryptedMsggmi = encrypt_ECC(byte_listticket,public_keygmi)
       encryptedMsgObjgmi = {
              'ciphertext': binascii.hexlify(encryptedMsggmi[0]),
              'nonce': binascii.hexlify(encryptedMsggmi[1]),
              'authTag': binascii.hexlify(encryptedMsggmi[2]),
              'ciphertextPubKey': hex(encryptedMsggmi[3].x) + hex(encryptedMsggmi[3].y % 2)[2:]
            }
       
       ticket[(mobileuseraddress,edgeserveraddress)]= encryptedMsggmi
       #print(" Show the keys in the ticket:",listticket)
       #print("ticket",ticket)
       #print("????????",encryptedMsggmi)
    else:
        print("Authentication failed")
    return ticket

## MU to MS first stage
def MuconectedtoMs1(mobileuseraddress,edgeserveraddress,ticket) :
    
    for key in Serverkeys.keys():
        if key==edgeserveraddress:# msi=gmi
           key_listserverAs= Serverkeys[key]
           private_keygmi=key_listserverAs[1]
           #print(private_keygmi)
    for key in ticket.keys():
       # print(key)
        if mobileuseraddress in key:
           if edgeserveraddress in key:
              #print("key",key)
              encryptedMsggmi=(ticket[key])
              #print(encryptedMsggmi)
             
           break
           print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
      
       
    decryptedMsghashticketgmi = decrypt_ECC(encryptedMsggmi,private_keygmi )
    pknmu=decryptedMsghashticketgmi[:271]
    pkmsi=decryptedMsghashticketgmi[271:]
    #print("pkn",pknmu)
   # print("pkmsi",pkmsi)
    #print("user",mobileuseraddress)
    #print("edge",edgeserveraddress)
    Eus = float(input('Enter Evaluation End user: '))
    Eus=Eus*100000000000000000
    Calculationofdirecttrust=reputation.DirectReputation(edgeserveraddress,mobileuseraddress,Eus,{"from": account})
    Calculationofindirecttrust=reputation.IndirectReputation(edgeserveraddress,mobileuseraddress,{"from": account})
    Rus=reputation.getRus({"from": account})
    wirteintoblockchain=mobilityuser.storeintheblockchain(mobileuseraddress,pknmu,Rus,{"from": account})

###########################################################################################################################


###########################################################################################################################
def Run():
   reputation.setaB(400000000000000000,600000000000000000,{"from": account})
  
   defult="0x0000000000000000000000000000000000000000"
   setMuconectedtoRc(defult)
   setMsconectedtoRc(defult)
   # address_user=["0xBe71f5F78398493D2b590cb325667240De5FBa85","0xb4E7A3ab310d42fa677c7fEC2c9e920ec3EA1EBD","0x3B024367EeDfcbab9dA24992E86472A4c743E5d4"]
   # address_server=["0x657092916E3cbF22548aA1367Cd612C35640e8ea","0x7B99dD41f4b9218d2f873B801e3Ef6d248C380e3"] 
   address_user=[]
   address_server=[]
   for i in range(1,4):
       mobileuseraddress=accounts[i] 
       address_user.append(mobileuseraddress)
   for i in range(6,8):
       edgeserveraddress=accounts[i]
       address_server.append(edgeserveraddress) 
   print("mobileuseraddress",address_user) 
   print("edgeserveraddress",address_server)
   for i in range(5):
       #mobileuseraddress=str(input(" Please enter the mobile user's address:" ))
       #edgeserveraddress=str(input(" Please enter the edge server's address:" ))
       mobileuseraddress= random.choice(address_user)
       edgeserveraddress=random.choice(address_server)
       print("mobileuseraddress",mobileuseraddress)
       print("edgeserveraddress",edgeserveraddress)
       MuconectedtoRc( mobileuseraddress)
       MsconectedtoRc(edgeserveraddress)
       GenerationAskeys()
       MuconectedtoNewMs1(mobileuseraddress,edgeserveraddress)
       MuconectedtoNewMs2(mobileuseraddress,edgeserveraddress)
       Readfromblockchain=mobilityuser.Researchpublickey(mobileuseraddress,{"from": account})
       result=mobilityuser.getResearchpublickey()
       print("result",result)
       
       


    
    

    

   

def main():
    Run()
   
    


