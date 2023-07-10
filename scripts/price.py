from random import *
from brownie import (   network,    accounts,    config,)
import random
import math

Edi={}
Esi={}
Save_users={}
User_request_cache={}
Save_users_interactions={}
count_t=1
address_user=[]
address_server=[]
dict_Server_capacity={}
list_selected_edgeserver=[]
dict_cost_caching_unitdatasize={}
def break_num2(num, count, mode="int"):
    if mode == "float":
        ingreds = [num / count for _ in range(count)]
    elif mode == "int":
        ingreds = [num // count for _ in range(count)]
    while count:
        i1 = randrange(len(ingreds))
        i2 = (i1 + 1) % len(ingreds)
        if mode == "float":
            n = uniform(0, ingreds[i1])
        elif mode == "int":
            n = randint(0, ingreds[i1])
        ingreds[i1] -= n
        ingreds[i2] += n
        count -= 1
    if sum(ingreds) < num:
        ingreds.append(num - sum(ingreds))
    return ingreds
def total_caching_demand_edgeserveri(edgeserveraddress):
    Edi[edgeserveraddress]=random.randrange(1, 10, 1) 
def Connecting_user_server(mobileuseraddress,edgeserveraddress):
    global count_t
    label="duplicate"
    Save_users[mobileuseraddress]=edgeserveraddress
    list_Save_users_interactions=[count_t,mobileuseraddress,label]
    Save_users_interactions[edgeserveraddress,count_t]=list_Save_users_interactions
    count_t=count_t+1
    print(" Save_users_interactions", Save_users_interactions)


def average_content_size_request(mobileuseraddress,edgeserveraddress):
    count=0
    mulfijsij=0
    fij=[]
    user_fij=[]
    sij=[]
    sumfijsij=0

    #Esi[mobileuseraddress,edgeserveraddress]=
    for j in range(0,len(list_selected_edgeserver)):

        for key in Save_users.keys():
            if Save_users[key]==list_selected_edgeserver[j]:
               count+=1
               user_fij.append(key)
        #print("user_fij",user_fij)
        #print("count",count)
        #print("lenuser",len(user_fij))

        fij=break_num2(1,count , "float")
        print("fij",fij)
        #print("lenfi",len(fij))

        for i in range(0,len(user_fij)):
            for key in User_request_cache.keys():
                if key==user_fij[i]:
                   sij.append(User_request_cache[key])
                  
        print("sij",sij)
        #print("lensi",len(sij))
    
        for i in range(0,len(user_fij)):
             mulfijsij=fij[i]*sij[i]
             sumfijsij +=mulfijsij
        #print("sumfijsij",sumfijsij)
    
        Esi[edgeserveraddress]=sumfijsij
        print("esi",Esi)
        count=0
        mulfijsij=0
        sumfijsij=0
        fij.clear()
        user_fij.clear()
        sij.clear()
    


        
def Calculate_price_parameter(edgeserveraddress):
    t=0
    n=0
    list_n=[]
    count_duplicate=1
    dict_user_duplicate={}
    list_duplicate=[]
    enT=0
    list_enT=[]
    Attenuation_parameter=0.1
    totalmul_ent_n=0
    Setting_parameter=1
    pi=0
    for j in range(0,len(list_selected_edgeserver)):
        for key in Save_users_interactions.keys():
            if list_selected_edgeserver[j] in key:
               t=t+1
        print("t",t)
        for key in Edi.keys():
            if key==list_selected_edgeserver[j]:
               edi=Edi[key]

        for key in Esi.keys():
            key==list_selected_edgeserver[j]
            esi=Esi[key]

        
        for k in range(0,len(address_user)):
            for key in Save_users_interactions.keys():
                if list_selected_edgeserver[j] in key:
                   list_user_duplicate=Save_users_interactions[key]
                   if address_user[k]==list_user_duplicate[1]:
                      list_duplicate=[count_duplicate,list_user_duplicate[1],list_user_duplicate[2]]
                      dict_user_duplicate[list_selected_edgeserver[j],count_duplicate]=list_duplicate
                      count_duplicate=count_duplicate+1
        #print(" first _dict_user_duplicate", dict_user_duplicate)
        for k in range(0,len(address_user)):
            for key in dict_user_duplicate.keys():
                remove_duplicate=dict_user_duplicate[key]
                if address_user[k]==remove_duplicate[1]:
                    remove_duplicate[2]="unique"
                    dict_user_duplicate[list_selected_edgeserver[j],remove_duplicate[0]]=[remove_duplicate[0],remove_duplicate[1],remove_duplicate[2]]
                    break
        #print(" secound_dict_user_duplicate", dict_user_duplicate)

        for k in range(0,len(address_user)):
            for key in dict_user_duplicate.keys():
                remove_duplicate_user=dict_user_duplicate[key]
                if remove_duplicate_user[2]=="duplicate":
                   remove_duplicate_user[1]="0x0000000000000000000000000000000000000000"
        
        #print("third_dict_user_duplicate", dict_user_duplicate)
        # data = dict_user_duplicate.pop(t)
        for key in dict_user_duplicate.keys():
            if t in key:
               data=key
        
        #print("final",data)
        dict_user_duplicate.pop(data)
        #print("finaldict_user_duplicate",dict_user_duplicate)
        for key in  dict_user_duplicate:
            list_number_users=dict_user_duplicate[key]
            if list_number_users[1] !="0x0000000000000000000000000000000000000000":
                 n=n+1
                 list_n.append(n)
            if list_number_users[1]=="0x0000000000000000000000000000000000000000":
                  list_n.append(n)

        #print("list_n",list_n)
        for i in range(1,t):
            subT=i-t
            mulT=Attenuation_parameter*subT
            enT=math.exp(mulT)
            enT+=enT
            list_enT.append(enT)
        total_enT=enT
        print("list_enT",list_enT)
        for i in range(0,len(list_n)):
            totalmul_ent_n= list_enT[i]*list_n[i]
            totalmul_ent_n +=totalmul_ent_n
        try:

            total=(Setting_parameter*total_enT)/(edi*esi*totalmul_ent_n )
        except:
              print("ZeroDivisionError")
        Price_parameter=math.log10(1+total)   
        print("Price_parameter",Price_parameter)
        for key in dict_Server_capacity.keys():
            if key==list_selected_edgeserver[j]:
                Ci=dict_Server_capacity[key]
        print("Ci",Ci)
        for key in dict_cost_caching_unitdatasize.keys():
            if key==list_selected_edgeserver[j]:
                ci=dict_cost_caching_unitdatasize[key]
        print("ci",ci)

        if Ci>=ci*Price_parameter:
            ciEi=ci*Price_parameter
            try:
                 pi=(Ci+ciEi)/2*Price_parameter
            except ZeroDivisionError:
                 print("ZeroDivisionError")
        else:
            pi=ci

        print("pi",pi)
        print("***************************************")
            



        
            
        dict_user_duplicate.clear()
        list_n.clear()
        list_enT.clear()
        t=0
        count_duplicate=1
        n=0
        enT=0
        totalmul_ent_n=0


                   

def Run():
    
   
    for i in range(1,4):
        mobileuseraddress=accounts[i] 
        address_user.append(mobileuseraddress)
        User_request_cache[mobileuseraddress]=random.randrange(40, 60, 1)
        print("User_request_cache",User_request_cache)
       
    for i in range(6,8):
       edgeserveraddress=accounts[i]
       address_server.append(edgeserveraddress)
       list_selected_edgeserver.append(edgeserveraddress)
       dict_Server_capacity[edgeserveraddress]=random.randrange(10, 60, 10) 
       dict_cost_caching_unitdatasize[edgeserveraddress]=random.randrange(1, 10, 1)


      
       
      
 
   #print("mobileuseraddress",address_user) 
   #print("edgeserveraddress",address_server)
    for i in range(6):

       #mobileuseraddress=str(input(" Please enter the mobile user's address:" ))
       #edgeserveraddress=str(input(" Please enter the edge server's address:" ))
       mobileuseraddress= random.choice(address_user)
       print("user",mobileuseraddress)
       edgeserveraddress=random.choice(address_server)
       print("edge server", edgeserveraddress)
       total_caching_demand_edgeserveri(edgeserveraddress)
       Connecting_user_server(mobileuseraddress,edgeserveraddress)
       average_content_size_request(mobileuseraddress,edgeserveraddress)
    Calculate_price_parameter(edgeserveraddress)









def main():
    Run()
