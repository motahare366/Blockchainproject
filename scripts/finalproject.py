from brownie import (network,    accounts,    config,)
import random
from random import randrange
from random import randint
from random import uniform
from brownie import Reputationcalculation, config, network
import math
import matplotlib.pyplot as plt
import numpy as np
dict_Calculations_graphs = {}
time = 0
dict_Server_status = {}
User_request_cache = {}
dict_Server_capacity = {}
User_fragment_cache = {}
dict_fragment_option = {}
index_list_fragment = {}
list_Saveuseraddress = []
dict_Saveuseraddress = {}
list_selected_edgeserver = []
count_g = 0
dict_allocate_server = {}
T = 1
############################
reputation_server = {}
threshold_Ti = 0.3
############################
Edi = {}
Esi = {}
Save_users = {}
Save_users_interactions = {}
count_t = 1
address_user = []
address_server = []
dict_pi = {}
dict_cost_caching_unitdatasize = {}
account = accounts[0]
reputation = Reputationcalculation.deploy({"from": account})


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


def max_min_fairness(demands, capacity):
    capacity_remaining = capacity
    output = []

    for i, demand in enumerate(demands):
        share = capacity_remaining / (len(demands) - i)
        allocation = min(share, demand)

        if i == len(demands) - 1:
            allocation = max(share, capacity_remaining)
            if capacity_remaining > demand:
                allocation = min(demand, capacity_remaining)

        output.append(allocation)
        capacity_remaining -= allocation
    return output, capacity_remaining


def Calculate_average_reputation():
    count_reputation = 0
    sum_reputation = 0
    average_reputation = 0
    for key in reputation_server.keys():
        count_reputation += 1
        sum_reputation = sum_reputation + \
            reputation_server[key]/1000000000000000000

    average_reputation = sum_reputation/count_reputation
    return average_reputation


def Choosing_optimal_server():
    a1 = 0.3
    a2 = 0.7
    dict_Deltai = {}
    list_Deltai = []
    list_Ti = []
    list_index_server = []
    global threshold_Ti

    for j in range(0, len(list_selected_edgeserver)):
        for key in dict_pi.keys():
            if key == list_selected_edgeserver[j]:
                server_pi = dict_pi[key]

        for key in reputation_server.keys():
            if key == list_selected_edgeserver[j]:
                server_Ti = reputation_server[key]
                server_Ti_float = server_Ti/1000000000000000000

        list_Ti.append(server_Ti_float)
        for key in dict_Server_capacity.keys():
            if key == list_selected_edgeserver[j]:
                server_Ci = dict_Server_capacity[key]
        print("server_Ci", server_Ci)
        print("list_selected_edgeserver[j]")
        sumTiCi1 = (a1 * server_Ti_float)
        print(" sumTiCi1", sumTiCi1)
        sumTiCi2 = (a2*server_Ci)
        print("sumTiCi2", sumTiCi2)
        sumTiCi = sumTiCi1+sumTiCi2
        Deltai = sumTiCi/server_pi
        dict_Deltai[list_selected_edgeserver[j]] = Deltai
        list_Deltai.append(Deltai)
        list_index_server.append(list_selected_edgeserver[j])

    for i in range(5):
        max_Deltai = max(list_Deltai)
        index_max = list_Deltai.index(max_Deltai)
        for key in reputation_server.keys():
            if key == list_index_server[index_max]:
                if list_Ti[index_max] >= threshold_Ti:
                   
                    Optimized_server = key
                   
                    break
                else:
                    list_Deltai.pop(index_max)
                    list_Ti.pop(index_max)
                    list_index_server.pop(index_max)

    dict_Deltai.clear()
    list_Deltai.clear()
    list_Ti.clear()
    list_index_server.clear()
    new_threshold_Ti = Calculate_average_reputation()
    #print("new_threshold_Ti", new_threshold_Ti)
    threshold_Ti = (0.2*threshold_Ti)+(0.8*new_threshold_Ti)
   # print("threshold_Ti", threshold_Ti)
    print("Optimized_server", Optimized_server)

    return Optimized_server


def setdefultFragmentationofUserContent(defult):
    total_capacity = 5
    splitsizecontent = break_num2(total_capacity, 3)
    User_fragment_cache[defult] = splitsizecontent


def setFragmentationofUserContent(mobileuseraddress):
    dict_Node = list(User_fragment_cache)
    search_item = mobileuseraddress
    found = False
    if search_item in dict_Node:
        found = True
    else:
        for key in User_request_cache.keys():
            if key == mobileuseraddress:
                total_capacity = User_request_cache[key]
                splitsizecontent = break_num2(total_capacity, 3)
                User_fragment_cache[mobileuseraddress] = splitsizecontent
                return User_fragment_cache[mobileuseraddress]


def setvalueandstatusFragmentationofUserContent(mobileuseraddress):
    status = "notassigned"
    status1 = "defective"

    for key in User_fragment_cache.keys():
        if key == mobileuseraddress:
            list_fragment = User_fragment_cache[mobileuseraddress]
    #print("list_fragment", list_fragment)
    for i in range(0, len(list_fragment)):
        if list_fragment[i] != 0:
            list_fragment_size = [i, list_fragment[i], status]
        else:
            list_fragment_size = [i, list_fragment[i], status1]

        dict_fragment_option[mobileuseraddress, i] = list_fragment_size
    return dict_fragment_option


def Saveuseraddress(mobileuseraddress, edgeserveraddress):
    global count_g
    dict_Saveuseraddress[edgeserveraddress, count_g] = mobileuseraddress
    count_g = count_g+1
    ################################################################################


def total_caching_demand_edgeserveri(mobileuseraddress, edgeserveraddress):
    sum_fragment = 0

    for key in dict_Saveuseraddress.keys():
        if edgeserveraddress in key:
            list_Saveuseraddress.append(dict_Saveuseraddress[key])
    for i in range(0, len(list_Saveuseraddress)):
        for key in dict_fragment_option.keys():
            if list_Saveuseraddress[i] in key:
                fragmentation_size = dict_fragment_option[key]

                if fragmentation_size[2] == "notassigned":
                    sum_fragment = sum_fragment+fragmentation_size[1]
                    break
                if fragmentation_size[2] == "remaining":
                    sum_fragment = sum_fragment+fragmentation_size[1]

    Edi[edgeserveraddress] = sum_fragment
    #print(" Edi", Edi)


def Connecting_user_server(mobileuseraddress, edgeserveraddress):
    global count_t
    label = "duplicate"
    Save_users[mobileuseraddress] = edgeserveraddress
    list_Save_users_interactions = [count_t, mobileuseraddress, label]
    Save_users_interactions[edgeserveraddress,
                            count_t] = list_Save_users_interactions
    count_t = count_t+1
    #print(" Save_users_interactions", Save_users_interactions)


def average_content_size_request(edgeserveraddress):
    count_f = 0
    mulfijsij = 0
    fij = []
    user_fij = []
    sij = []
    sumfijsij = 0

    for key in Save_users.keys():
        if Save_users[key] == edgeserveraddress:
            count_f = count_f+1
            user_fij.append(key)
        print("user_fij", user_fij)
        print("count", count_f)

    fij = break_num2(1, count_f, "float")
    print("fij", fij)
    for i in range(0, len(user_fij)):
        for key in User_request_cache.keys():
            if key == user_fij[i]:
                sij.append(User_request_cache[key])

    #print("sij", sij)
    for i in range(0, len(user_fij)):
        mulfijsij = fij[i]*sij[i]
        sumfijsij += mulfijsij
    Esi[edgeserveraddress] = sumfijsij
    print("esi", Esi)
    count_f = 0
    mulfijsij = 0
    sumfijsij = 0
    fij.clear()
    user_fij.clear()
    sij.clear()


def Calculate_price_parameter(edgeserveraddress):
    t = 0
    n = 0
    list_n = []
    count_duplicate = 1
    dict_user_duplicate = {}
    list_duplicate = []
    enT = 0
    list_enT = []
    Attenuation_parameter = 0.1
    totalmul_ent_n = 0
    Setting_parameter = 1000
    pi = 0

    for key in Save_users_interactions.keys():
        if edgeserveraddress in key:
            t = t+1
    print("t", t)
    for key in Edi.keys():
        if key == edgeserveraddress:
            edi = Edi[key]

    for key in Esi.keys():
        key == edgeserveraddress
        esi = Esi[key]

    for k in range(0, len(address_user)):
        for key in Save_users_interactions.keys():
            if edgeserveraddress in key:
                list_user_duplicate = Save_users_interactions[key]
                if address_user[k] == list_user_duplicate[1]:
                    list_duplicate = [
                        count_duplicate, list_user_duplicate[1], list_user_duplicate[2]]
                    dict_user_duplicate[edgeserveraddress,
                                        count_duplicate] = list_duplicate
                    count_duplicate = count_duplicate+1
    for k in range(0, len(address_user)):
        for key in dict_user_duplicate.keys():
            remove_duplicate = dict_user_duplicate[key]
            if address_user[k] == remove_duplicate[1]:
                remove_duplicate[2] = "unique"
                dict_user_duplicate[edgeserveraddress, remove_duplicate[0]] = [
                    remove_duplicate[0], remove_duplicate[1], remove_duplicate[2]]
                break

    for k in range(0, len(address_user)):
        for key in dict_user_duplicate.keys():
            remove_duplicate_user = dict_user_duplicate[key]
            if remove_duplicate_user[2] == "duplicate":
                remove_duplicate_user[1] = "0x0000000000000000000000000000000000000000"

    for key in dict_user_duplicate.keys():
        if t in key:
            data = key

    if len(dict_user_duplicate) != 0:
        dict_user_duplicate.pop(data)
        for key in dict_user_duplicate:
            list_number_users = dict_user_duplicate[key]
            if list_number_users[1] != "0x0000000000000000000000000000000000000000":
                n = n+1
                list_n.append(n)
            if list_number_users[1] == "0x0000000000000000000000000000000000000000":
                list_n.append(n)

        for i in range(1, t):
            subT = i-t
            mulT = Attenuation_parameter*subT
            enT = math.exp(mulT)
            enT += enT
            list_enT.append(enT)
        total_enT = enT
        #print("list_enT", list_enT)
        for i in range(0, len(list_n)):
            totalmul_ent_n = list_enT[i]*list_n[i]
            totalmul_ent_n += totalmul_ent_n
        try:

            total = (Setting_parameter*total_enT)/(edi*esi*totalmul_ent_n)
        except:
            print("ZeroDivisionError")
        Price_parameter = math.log10(1+total)
        #print("Price_parameter", Price_parameter)
        for key in dict_Server_capacity.keys():
            if key == edgeserveraddress:
                Ci = dict_Server_capacity[key]
        #print("Ci", Ci)
        for key in dict_cost_caching_unitdatasize.keys():
            if key == edgeserveraddress:
                ci = dict_cost_caching_unitdatasize[key]
       # print("ci", ci)

        if Ci >= ci*Price_parameter:
            ciEi = ci*Price_parameter
            try:
                pi = (Ci+ciEi)/2*Price_parameter
            except ZeroDivisionError:
                print("ZeroDivisionError")
        else:
            pi = ci

        #print("pi", pi)
        dict_pi[edgeserveraddress] = pi
        print("***************************************")

    dict_user_duplicate.clear()
    list_n.clear()
    list_enT.clear()
    t = 0
    count_duplicate = 1
    n = 0
    enT = 0
    totalmul_ent_n = 0


def Sendfragmentedusercontenttotheserver(edgeserveraddress):
    demands = []
    dict_demands = {}
    index = 0
    list_index = []
    list_Saveuseraddress = []

    for key in dict_Saveuseraddress.keys():
        if edgeserveraddress in key:
            list_Saveuseraddress.append(dict_Saveuseraddress[key])
    for key in dict_Server_status.keys():
        if key == edgeserveraddress:
            status = dict_Server_status[key]
            print("list_selected_edgeserver[j]", edgeserveraddress)
            if status == "malicious":
                print("status", status)
                for i in range(0, len(list_Saveuseraddress)):
                    Eus = 0
                    print("Eus", Eus)
                    print("edgeserveraddress", edgeserveraddress)
                    print("list_Saveuseraddress[i]", list_Saveuseraddress[i])
                    Calculationofdirecttrust = reputation.DirectReputation(
                        edgeserveraddress, list_Saveuseraddress[i], Eus, {"from": account})
                    print(Calculationofdirecttrust.events)
                   
            if status == "low_quality":
                print("status", status)
                for i in range(0, len(list_Saveuseraddress)):
                    Eus = random.uniform(0, 0.3)
                    print("Eus", Eus)
                    print("edgeserveraddress", edgeserveraddress)
                    print("list_Saveuseraddress[i]", list_Saveuseraddress[i])
                    Eus = Eus*1000000000000000000
                    Calculationofdirecttrust = reputation.DirectReputation(
                        edgeserveraddress, list_Saveuseraddress[i], Eus, {"from": account})
                    print(Calculationofdirecttrust.events)
                  
            if status == "high_quality":
                print("status", status)
                for i in range(0, len(list_Saveuseraddress)):
                    Eus = random.uniform(0.8, 1)
                    print("Eus", Eus)
                    print("edgeserveraddress", edgeserveraddress)
                    print("list_Saveuseraddress[i]", list_Saveuseraddress[i])
                    Eus = Eus*1000000000000000000
                    Calculationofdirecttrust = reputation.DirectReputation(
                        edgeserveraddress, list_Saveuseraddress[i], Eus, {"from": account})
                    print(Calculationofdirecttrust.events)
                    
    for i in range(0, len(list_Saveuseraddress)):
        for key in dict_fragment_option.keys():
            if list_Saveuseraddress[i] in key:
                fragmentation_size = dict_fragment_option[key]
                print(
                    f" {list_Saveuseraddress[i]} is selected {fragmentation_size} ")

                if fragmentation_size[2] == "notassigned":
                    print("dict Not assigned", dict_fragment_option)
                    fragmentation_size[2] = "uncertain"
                    demands.append(fragmentation_size[1])
                    list_index = [index, fragmentation_size[0],
                                  fragmentation_size[1]]
                    dict_demands[list_Saveuseraddress[i],
                                 fragmentation_size[0]] = list_index
                    dict_fragment_option[list_Saveuseraddress[i], fragmentation_size[0]] = [
                        fragmentation_size[0], fragmentation_size[1], fragmentation_size[2]]
                    index = index+1
                    break

                    if fragmentation_size[2] == "remaining":
                        print("dict", dict_fragment_option)
                        fragmentation_size[2] = "uncertain"
                        demands.append(fragmentation_size[1])
                        list_index = [
                            index, fragmentation_size[0], fragmentation_size[1]]
                        dict_demands[list_Saveuseraddress[i],
                                     fragmentation_size[0]] = list_index
                        dict_fragment_option[list_Saveuseraddress[i], fragmentation_size[0]] = [
                            fragmentation_size[0], fragmentation_size[1], fragmentation_size[2]]
                        index = index+1
                        break

    for key in dict_Server_capacity.keys():
        if key == edgeserveraddress:
            Server_capacity = dict_Server_capacity[edgeserveraddress]
            print("Initial server capacity", Server_capacity)
            print("User demand", demands)
            result = max_min_fairness(demands, Server_capacity)
            Remaining_server_capacity = result[1]
            dict_allocate_server[edgeserveraddress] = Remaining_server_capacity
            list_assigned_content = result[0]
    for key in dict_Server_capacity.keys():
        if key == edgeserveraddress:
            dict_Server_capacity[edgeserveraddress] = Remaining_server_capacity
            print("Remaining server capacity",dict_Server_capacity[edgeserveraddress])
                  
    for i in range(0, len(list_Saveuseraddress)):
        for key in dict_demands.keys():
            if list_Saveuseraddress[i] in key:
                dict_demands_user = dict_demands[key]
                index_demand = dict_demands_user[0]
                id_demand = dict_demands_user[1]
                size_demand = dict_demands_user[2]
                assigned_content = list_assigned_content[index_demand]
                if size_demand > assigned_content:
                    remaining_content = size_demand - assigned_content
                else:
                    remaining_content = assigned_content - size_demand
                if (remaining_content == 0):
                    status = "allocated"
                else:
                    status = "remaining"

                dict_fragment_option[list_Saveuseraddress[i], id_demand] = [
                    id_demand, remaining_content, status]
    dict_Saveuseraddress.clear()
    print("remain or allocate ", dict_fragment_option)


def time_attenuation_factor(mobileuseraddress, edgeserveraddress):
    global T
    T = T+1
    print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTt", T)
    if T % 2 == 0:
        c = reputation.IndirectReputation(
            address_user, edgeserveraddress, mobileuseraddress, {"from": account})
        print(c.events)
        Rus = reputation.getRus({"from": account})
        reputation_server[edgeserveraddress] = Rus


def Calculations_graphs():
    global time
    for i in range(0, len(list_selected_edgeserver)):
        for key in dict_Server_status.keys():
            if key == list_selected_edgeserver[i]:
                status = dict_Server_status[key]

        for key in reputation_server.keys():
            if key == list_selected_edgeserver[i]:
                reputation_total = reputation_server[key]
        for key in dict_pi.keys():
            if key == list_selected_edgeserver[i]:
                price = dict_pi[key]

        for key in dict_Server_capacity.keys():
            if key == list_selected_edgeserver[i]:
                capacityserver = dict_Server_capacity[key]

        for key in dict_allocate_server.keys():
            if key == list_selected_edgeserver[i]:
                allocate = dict_allocate_server[key]

        for key in Edi.keys():
            if key == list_selected_edgeserver[i]:
                demand_server = Edi[key]

        for key in Esi.keys():
            if key == list_selected_edgeserver[i]:
                Content_size = Esi[key]
        list_Calculations_graphs = [
            time, status, reputation_total, price, capacityserver, allocate, demand_server]
        dict_Calculations_graphs[(
            list_selected_edgeserver[i], time)] = list_Calculations_graphs
    time = time+1
    print("graph", dict_Calculations_graphs)


def Calculation_average_project_parameters():
    list_time = []
    count_malicious = 0
    count_low_quality = 0
    count_high_quality = 0
    sum_chachingprice_malicious = 0
    sum_chachingprice_low_quality = 0
    sum_chachingprice_high_quality = 0
    average_chachingprice_malicious = 0
    average_chachingprice_low_quality = 0
    avarage_chachingprice_high_quality = 0
    list_average_chachingprice_malicious = []
    list_average_chachingprice_low_quality = []
    list_avarage_chachingprice_high_quality = []

    for i in range(0, time):

        list_time.append(i)

        for key in dict_Calculations_graphs.keys():
            if i in key:
                Calculations_graphs = dict_Calculations_graphs[key]
                if Calculations_graphs[1] == "malicious":
                    count_malicious += 1
                    sum_chachingprice_malicious = sum_chachingprice_malicious + \
                        Calculations_graphs[3]
                if Calculations_graphs[1] == "low_quality":
                    count_low_quality += 1
                    sum_chachingprice_low_quality = sum_chachingprice_low_quality + \
                        Calculations_graphs[3]
                if Calculations_graphs[1] == "high_quality":
                    count_high_quality += 1
                    sum_chachingprice_high_quality = sum_chachingprice_high_quality + \
                        Calculations_graphs[3]
        average_chachingprice_malicious = sum_chachingprice_malicious/count_malicious
        average_chachingprice_low_quality = sum_chachingprice_low_quality/count_low_quality
        avarage_chachingprice_high_quality = sum_chachingprice_high_quality/count_high_quality
        list_average_chachingprice_malicious.append(
            average_chachingprice_malicious)
        list_average_chachingprice_low_quality.append(
            average_chachingprice_low_quality)
        list_avarage_chachingprice_high_quality.append(
            avarage_chachingprice_high_quality)
        count_malicious = 0
        count_low_quality = 0
        count_high_quality = 0
        sum_chachingprice_malicious = 0
        sum_chachingprice_low_quality = 0
        sum_chachingprice_high_quality = 0
        average_chachingprice_malicious = 0
        average_chachingprice_low_quality = 0
        avarage_chachingprice_high_quality = 0

    fig, ax = plt.subplots()
    if i == 0:
        xpoints = np.array(0)
        ypoints = np.array(list_average_chachingprice_malicious)
        ax.plot(xpoints, ypoints, '--bo', color='r',
                label='Malicious edge nodes')
        ypoints = np.array(list_average_chachingprice_low_quality)
        ax.plot(xpoints, ypoints, '--bo', color='b',
                label='Low_quality edge nodes')
        ypoints = np.array(list_avarage_chachingprice_high_quality)
        ax.plot(xpoints, ypoints, '--bo', color='g',
                label='High_quality edge nodes')
    else:
        xpoints = np.array(list_time)
        ypoints = np.array(list_average_chachingprice_malicious)
        ax.plot(xpoints, ypoints, '--bo', color='r',
                label='Malicious edge nodes')
        ypoints = np.array(list_average_chachingprice_low_quality)
        ax.plot(xpoints, ypoints, '--bo', color='b',
                label='Low_quality edge nodes')
        ypoints = np.array(list_avarage_chachingprice_high_quality)
        ax.plot(xpoints, ypoints, '--bo', color='g',
                label='High_quality edge nodes')

    plt.xlabel('Simulation time')
    plt.ylabel('Caching price')
    ax.set_title("Caching price of edge node vs. simulation time")
    ax.legend()
    fig.tight_layout()
    plt.grid()
    plt.show()


def Calculate_draw_reputation_chart():
    list_time = []
    count_malicious = 0
    count_low_quality = 0
    count_high_quality = 0
    sum_reputation_malicious = 0
    sum_reputation_low_quality = 0
    sum_reputation_high_quality = 0
    average_reputation_malicious = 0
    average_reputation_low_quality = 0
    avarage_reputation_high_quality = 0
    list_average_reputation_malicious = []
    list_average_reputation_low_quality = []
    list_avarage_reputation_high_quality = []

    for i in range(0, time):

        list_time.append(i)

        for key in dict_Calculations_graphs.keys():
            if i in key:
                Calculations_graphs = dict_Calculations_graphs[key]
                if Calculations_graphs[1] == "malicious":
                    count_malicious += 1
                    sum_reputation_malicious = sum_reputation_malicious + Calculations_graphs[2]
                       
                if Calculations_graphs[1] == "low_quality":
                    count_low_quality += 1
                    sum_reputation_low_quality = sum_reputation_low_quality + Calculations_graphs[2]
                       
                if Calculations_graphs[1] == "high_quality":
                    count_high_quality += 1
                    sum_reputation_high_quality = sum_reputation_high_quality + Calculations_graphs[2]
                       
        
        sum_reputation_malicious = sum_reputation_malicious/1000000000000000000
        average_reputation_malicious = sum_reputation_malicious/count_malicious
        sum_reputation_low_quality = sum_reputation_low_quality/1000000000000000000
        average_reputation_low_quality = sum_reputation_low_quality/count_low_quality
        sum_reputation_high_quality = sum_reputation_high_quality/1000000000000000000
        avarage_reputation_high_quality = sum_reputation_high_quality/count_high_quality
        list_average_reputation_malicious.append(average_reputation_malicious)
        list_average_reputation_low_quality.append(
            average_reputation_low_quality)
        list_avarage_reputation_high_quality.append(
            avarage_reputation_high_quality)
        count_malicious = 0
        count_low_quality = 0
        count_high_quality = 0
        sum_reputation_malicious = 0
        sum_reputation_low_quality = 0
        sum_reputation_high_quality = 0
        average_reputation_malicious = 0
        average_reputation_low_quality = 0
        avarage_reputation_high_quality = 0

    fig, ax = plt.subplots()
    if i == 0:
        xpoints = np.array(0)
        ypoints = np.array(list_average_reputation_malicious)
        ax.plot(xpoints, ypoints, '--bo', color='r',
                label='Malicious edge nodes')
        ypoints = np.array(list_average_reputation_low_quality)
        ax.plot(xpoints, ypoints, '--bo', color='b',
                label='Low_quality edge nodes')
        ypoints = np.array(list_avarage_reputation_high_quality)
        ax.plot(xpoints, ypoints, '--bo', color='g',
                label='High_quality edge nodes')
    else:
        xpoints = np.array(list_time)
        ypoints = np.array(list_average_reputation_malicious)
        ax.plot(xpoints, ypoints, '--bo', color='r',
                label='Malicious edge nodes')
        ypoints = np.array(list_average_reputation_low_quality)
        ax.plot(xpoints, ypoints, '--bo', color='b',
                label='Low_quality edge nodes')
        ypoints = np.array(list_avarage_reputation_high_quality)
        ax.plot(xpoints, ypoints, '--bo', color='g',
                label='High_quality edge nodes')

    plt.xlabel('Simulation time')
    plt.ylabel('Average trust degree of the edge node')
    ax.set_title("Average trust degree of edge node vs. simulation time")
    ax.legend()
    fig.tight_layout()
    plt.grid()
    plt.show()


def Run():

    reputation.setaB(400000000000000000, 600000000000000000, {"from": account})
    defult = "0x0000000000000000000000000000000000000000"

    setdefultFragmentationofUserContent(defult)
    for i in range(1, 8):
        mobileuseraddress = accounts[i]
        address_user.append(mobileuseraddress)
        User_request_cache[mobileuseraddress] = random.randrange(1, 10, 1)
        #User_request_cache[mobileuseraddress] = 10
        User_fragment_cache = setFragmentationofUserContent(mobileuseraddress)

    print("user", User_request_cache)

    for i in range(10, 12):
        status = "malicious"
        edgeserveraddress = accounts[i]
        address_server.append(edgeserveraddress)
        list_selected_edgeserver.append(edgeserveraddress)
        # dict_Server_capacity[edgeserveraddress]=random.randrange(60, 100, 10)
        dict_Server_capacity[edgeserveraddress] = 50
        dict_pi[edgeserveraddress] = 1
        dict_cost_caching_unitdatasize[edgeserveraddress] = 1
        reputation_server[edgeserveraddress] = 300000000000000000
        dict_Server_status[edgeserveraddress] = status
        dict_allocate_server[edgeserveraddress] = 0
        Edi[edgeserveraddress] = 0

    for i in range(12, 14):
        status = "low_quality"
        edgeserveraddress = accounts[i]
        address_server.append(edgeserveraddress)
        list_selected_edgeserver.append(edgeserveraddress)
        # dict_Server_capacity[edgeserveraddress]=random.randrange(60, 100, 10)
        dict_Server_capacity[edgeserveraddress] = 50
        dict_pi[edgeserveraddress] = 1
        dict_cost_caching_unitdatasize[edgeserveraddress] = 1
        reputation_server[edgeserveraddress] = 300000000000000000
        dict_Server_status[edgeserveraddress] = status
        dict_allocate_server[edgeserveraddress] = 0
        Edi[edgeserveraddress] = 0

    for i in range(14,18):
        status = "high_quality"
        edgeserveraddress = accounts[i]
        address_server.append(edgeserveraddress)
        list_selected_edgeserver.append(edgeserveraddress)
        # dict_Server_capacity[edgeserveraddress]=random.randrange(60,100, 10)
        dict_Server_capacity[edgeserveraddress] = 50
        dict_pi[edgeserveraddress] = 1
        dict_cost_caching_unitdatasize[edgeserveraddress] = 1
        reputation_server[edgeserveraddress] = 300000000000000000
        dict_Server_status[edgeserveraddress] = status
        dict_allocate_server[edgeserveraddress] = 0
        Edi[edgeserveraddress] = 0

        print("server", dict_Server_capacity)

    # print("mobileuseraddress",address_user)
    # print("edgeserveraddress",address_server)
    for i in range(14):

        
        edgeserveraddress = Choosing_optimal_server()
        for j in range(5):
            # edgeserveraddress=Choosing_optimal_server()
            mobileuseraddress = random.choice(address_user)
            print("user", mobileuseraddress)

            setFragmentationofUserContent(mobileuseraddress)
            dict_fragment_option = setvalueandstatusFragmentationofUserContent(
                mobileuseraddress)
            print("##############")
            Saveuseraddress(mobileuseraddress, edgeserveraddress)
            #########################

            total_caching_demand_edgeserveri(
                mobileuseraddress, edgeserveraddress)
            Connecting_user_server(mobileuseraddress, edgeserveraddress)
            average_content_size_request(edgeserveraddress)
        Calculate_price_parameter(edgeserveraddress)
        Sendfragmentedusercontenttotheserver(edgeserveraddress)
        time_attenuation_factor(mobileuseraddress, edgeserveraddress)
        Calculations_graphs()


def main():

    Run()
    Calculation_average_project_parameters()
    Calculate_draw_reputation_chart()
