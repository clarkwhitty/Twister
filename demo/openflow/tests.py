import pprint
import json
import time
from oflib import *

switch_3="00:00:00:00:00:00:00:03"
switch_4="00:00:00:00:00:00:00:04"
switch_5="00:00:00:00:00:00:00:05"


initial_flow_path=[(switch_3,1,2),(switch_3,2,1),(switch_4,1,2),(switch_4,2,1)]
changed_flow_path=[(switch_3,1,3),(switch_3,3,1),(switch_5,1,2),(switch_5,2,1),(switch_4,1,3),(switch_4,3,1)]

def of_floodlight_1():
    log_debug("Starting openflow controller test 1")
    log_debug("Getting switches connected to floodlight controler")
    res=restapi.get_switches()
    print res
    if(res[0]==200):
        of_dict=json.loads(res[2])
        for sid in of_dict:
            print sid;
    else:
        return False    
    return True;
    
def of_floodlight_2():
    print "Starting openflow controller test 2"
    print "Getting agregate stats from floodlight controler"            
    res=restapi.get_aggregate_stats("flow")
    print res
    return True

#statType: port, queue, flow, aggregate, desc, table, features, host    
#Get port statistics
def of_floodlight_3():
    print "Starting openflow controller test 3"
    statsType="port"
    #Getting registered swiches
    fl_switches=restapi.get_switches()    
    if(statsType=="port"):
        print "Getting port statistics from floodlight controller\n"
        for sw in fl_switches:
            switch_dpid=sw['dpid']
            print "Swich DPID: %s" % switch_dpid        
            of_dict=restapi.get_switch_statistics(switch_dpid,statsType)
            if(of_dict!=None):
                port_stats=of_dict[switch_dpid]
                for ps in  port_stats:
                    if(ps['portNumber'] <0):
                        continue
                    print "portNumber:      %s" % ps['portNumber']
                    print "transmitPackets: %s" % ps['transmitPackets']
                    print "transmitBytes:   %s" % ps['transmitBytes']
                    print "receivePackets:  %s" % ps['receivePackets']
                    print "receiveBytes:    %s" % ps['receiveBytes']
                    print "\n"
                    #print "portNumber:%s tx_pkt: %d tx_bytes: %d rx_pkt: %s rx_bytes: %i" % \
                    #(ps['portNumber'],ps['transmitPackets'], ps['transmitBytes'],ps['receivePackets'], ps['receiveBytes'])
            else:
                return False  
    return True;
    
#Get flows from floodlight controller    
def of_floodlight_4():    
    statsType="flow"
    print "Starting openflow controller test 4"
    fl_switches=restapi.get_switches()
    if(statsType=="flow"):
        print "Getting flows from floodlight controller \n"
        for sw in fl_switches:
            switch_dpid=sw['dpid']
            print "Swich DPID: %s" % switch_dpid        
            fl_dict=restapi.get_switch_statistics(switch_dpid,statsType)
            #print fl_dict
            if(fl_dict!=None):
                flows=fl_dict[switch_dpid]                
                for fl in flows:                     
                     match=fl['match']
                     print "Match:"
                     for key,value in match.items():
                            print "   %s:%s" % (key,value)
                     actions=fl['actions']
                     for act in actions:                                             
                        print "Action:"
                        for key,value in act.items():
                            print "   %s:%s" % (key,value)
            else:
                return False            
            print "\n"
    return True;
    
def of_floodlight_5():
    log_debug("Starting openflow controller test 5\n")
    log_debug("Getting topology links from floodlight controler")
    topo_links=restapi.get_topology_links()    
    for tl in topo_links:        
        log_debug("src-swich: %s -> dst-switch: %s" % (tl['src-switch'],tl['dst-switch']))
        log_debug("src-port: %s -> dst-port: %s\n" % (tl['src-port'],tl['dst-port']))
    log_debug("Done.\n")
#    print topo_links

# adding flow path to controler, wait 10 secons
# then remove flow path, the flow path should be added on both swiches
# Assume that the topology is known
def of_floodlight_6():
    print "Starting openflow controller test 6"
    print "Getting registered switches to controler:"
    fl_switches=restapi.get_switches()
    for s in fl_switches:
       print "DPID: %s" % s['dpid']   
    log_debug("Adding initial flows path")    
    #flow_struct={"switch":"","name":"flow_1","ingress-port":"1","active":"true","actions":"output=2"}
    fl_list=[]
    fl_nr=0
    for ifp in initial_flow_path: 
        fl_nr+=1
        fl_name="flow-mod-%i" % fl_nr        
        fl_dict={"switch":ifp[0],"name":fl_name,"cookie":"0","priority":"32768","ingress-port":str(ifp[1]),"active":"true","actions":"output=%i" % ifp[2]}        
        fl_list.append(fl_dict);
    log_debug("Done.\n")
    
    
    log_debug("Getting flows from controller")
    of_floodlight_4()            
    log_debug("Push new flow to controler")
    for fl in fl_list:
        flowpusher.set(fl)
        time.sleep(1)
        log_debug("Flow added:\n %s"% str(fl))                
    tm_wait=30    
    log_debug("Getting flows from controller")
    of_floodlight_4()        
    log_debug ("\nSleep %i seconds before removing the flows\n" % tm_wait)
        
    time.sleep(tm_wait)
    
    log_debug ("Removing datapath flows \n")
    for fl in fl_list:
        flowpusher.remove(None,fl)
        time.sleep(1)
        log_debug("Flow removed:\n %s"% str(fl)) 
    log_debug("Getting flows from controller")
    of_floodlight_4()        
    
def of_floodlight_7():
    print "Starting openflow controller test 7"
    print "Getting registered switches to controler:"    
    fl_switches=restapi.get_switches()
    for s in fl_switches:
       print "DPID: %s" % s['dpid']   
    log_debug("Change flows path")
    fl_list=[]
    fl_nr=0
    for ifp in changed_flow_path: 
        fl_nr+=1
        fl_name="flow-mod-%i" % fl_nr        
        fl_dict={"switch":ifp[0],"name":fl_name,"cookie":"0","priority":"32768","ingress-port":str(ifp[1]),"active":"true","actions":"output=%i" % ifp[2]}        
        fl_list.append(fl_dict);
    log_debug("Done.\n")
    log_debug("Getting flows from controller")
    of_floodlight_4()            
    log_debug("Push new flow to controler")
    for fl in fl_list:
        flowpusher.set(fl)
        log_debug("Flow added:\n %s"% str(fl))                
    tm_wait=30    
    log_debug("Getting flows from controller")
    of_floodlight_4()        
    log_debug ("\nSleep %i seconds before removing the flows\n" % tm_wait)
    time.sleep(tm_wait)    
    log_debug ("Removing datapath flows \n")
    for fl in fl_list:
        flowpusher.remove(None,fl)
        log_debug("Flow removed:\n %s"% str(fl)) 
    log_debug("Getting flows from controller")
    of_floodlight_4()  

restapi= RestApiTest('11.126.32.12',8080)
flowpusher = StaticFlowPusher('11.126.32.12')
          
#of_floodlight_1()
#of_floodlight_2()
#of_floodlight_3()
#of_floodlight_4()
#of_floodlight_5()
#of_floodlight_6()
of_floodlight_7()


