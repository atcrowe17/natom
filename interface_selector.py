import re
import os

#requests the Cisco configuration text file name
#file_name = input("File Name:")
#print(file_name)

def add_to_interface_dict(interface):
    interface_dict['interface_table'].append(interface)

def id_software_ver(open_config_file):
    re_sw_xr = re.compile(r'(^.*IOS XR.*\n)', re.M)
    execute_re = re_sw_xr.finditer(open_config_file)
    # result =
    # re_get_sw = re.compile(r'^!! IOS XR.*', re.M).search(execute_re)
    # result_value = result.group
    for result in execute_re:
        result_value = result.group()
        if "IOS XR" in result_value:
            return('xr')
        else:
            return('xe')

#Takes a Cisco config file and creates a file called re_results.txt with just the interface configs
def ints_from_config (config_file):
    file_open = open(config_file)
    print(file_open)
    #matches interface configuration sections
    re_get_ints = re.compile(r'(?<=!\n)(interface.*\n)(.*\n)*?(?=!)', re.M)
    read_config = file_open.read()
    sw_ver = id_software_ver(read_config)
    execute_re = re_get_ints.finditer(read_config)
    print(sw_ver)
    if sw_ver == 'xr':
        for result in execute_re:
            result_value = result.group()
            re_int_label = re.compile(r'interface.*').match(result_value)
            re_shut_xr_int = re.compile(r'^.shutdown.*', re.M).search(result_value)
            re_l3_xr_int = re.compile(r'^.ipv4 address.*', re.M).search(result_value)
            re_loop_xr_int = re.compile(r'^interface Loopback.*', re.M).search(result_value)
            re_tun_xr_int = re.compile(r'^interface tunnel-ip.*', re.M).search(result_value)
            if re_shut_xr_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "shut_xr"
            #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_loop_xr_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "loop_xr"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_tun_xr_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "tun_xr"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_l3_xr_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "l3_xr"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            else:
                pass
    else:
        for result in execute_re:
            result_value = result.group()
            re_int_label = re.compile(r'interface.*').match(result_value)
            re_shut_int = re.compile(r'^.shutdown.*', re.M).search(result_value)
            re_l3_vlan_int = re.compile(r'interface Vlan.*', re.M).search(result_value)
            re_access_int = re.compile(r'^.switchport mode access.*', re.M).search(result_value)
            re_trunk_int = re.compile(r'^.switchport mode trunk.*', re.M).search(result_value)
            re_l3_xe_int = re.compile(r'^.ip address.*', re.M).search(result_value)
            re_no_ip_xe_int = re.compile(r'^.no switchport.*', re.M).search(result_value)
            re_loop_xe_int = re.compile(r'^interface Loopback.*', re.M).search(result_value)
            re_tun_xe_int = re.compile(r'^interface Tunnel.*', re.M).search(result_value)
            if re_shut_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "shutdown"
            #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_l3_vlan_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "l3_vlan"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_access_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "l2_access"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_trunk_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "l2_dot1q"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_loop_xe_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "loop_xe"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_tun_xe_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "tun_xe"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_l3_xe_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "l3_xe"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            elif re_no_ip_xe_int != None:
                interface = {}
                interface['label'] = re_int_label.group()
                interface['type'] = "l3_no_ip"
                #            interface['location'] = "internal" "external"
                print(interface)
                add_to_interface_dict(interface)
            else:
                pass

def config_gen_shut_xe (shut_xe_int):
    shut_xe_config_list = ["default " + shut_xe_int['label'] + "\n", shut_xe_int['label'] + "\n",
                            " description <== DISABLED ==>\n", " switchport access vlan 2\n",
                            " switchport mode access\n", " no logging event link-status\n", " shutdown\n",
                            " no cdp enable\n", " no snmp trap link-status\n", "!\n"]
    return(shut_xe_config_list)

def config_gen_shut_xr (shut_xr_int):
    shut_xr_config_list = [shut_xr_int['label'] + "\n", " description <== DISABLED ==>\n",
                           " ipv4 unreachables disable\n", " no ipv4 directed-broadcast\n",
                           " no ipv4 mask-reply\n", " no ipv4 redirects\n", " lldp transmit disable\n",
                           " lldp receive disable\n", " shutdown\n", "!\n"]
    return(shut_xr_config_list)

def config_gen_l2_access (l2_access_int):
    l2_access_config_list = [l2_access_int['label'] + "\n", " no cdp enable\n", " no lldp receive\n",
                             " no lldp transmist\n", "\n", " spanning-tree portfast edge\n", "!\n"]
    return(l2_access_config_list)

def config_gen_l2_dot1q (l2_dot1q_int):
    l2_dot1q_config_list = [l2_dot1q_int['label'] + "\n", " no storm-control unicast\n",
                            " no storm-control broadcast\n", " no spanning-tree guard root\n",
                            " no spanning-tree portfast\n", "!\n"]
    return(l2_dot1q_config_list)

def config_gen_ints_xe_l3(xe_l3_int):
    xe_l3_config_list = [xe_l3_int['label'] + "\n", " no ip mask-reply\n",
                         " no ip redirects\n", " no ip proxy-arp\n", " no lldp transmit\n", " no lldp receive\n", "!\n"]
    return(xe_l3_config_list)

def config_gen_ints_xr_l3(xr_l3_int):
    xr_l3_config_list = [xr_l3_int['label'] + "\n", " ipv4 unreachables disable\n", " no ipv4 directed-broadcast\n",
                         " no ipv4 mask-reply\n", " no ipv4 redirects\n", " lldp transmit disable\n",
                         " lldp receive disable\n", "!\n"]
    return(xr_l3_config_list)

def config_gen_ints_l3_vlan(l3_vlan_int):
    l3_vlan_config_list = [l3_vlan_int['label'] + "\n", " #this should be a vlan interface\n", " no ip unreachables\n",
                           " no ip mask-reply\n", " no ip redirects\n", " no ip proxy-arp\n",
                           " no lldp transmit\n", "!\n"]
    return(l3_vlan_config_list)

def config_gen_ints_l3_no_ip_xe(l3_no_ip_xe_int):
    l3_no_ip_xe_config_list = [l3_no_ip_xe_int['label'] + "\n",
                               " #this should be an L3 int w/o an ip interface\n", " no ip unreachables\n",
                               " no ip mask-reply\n", " no ip redirects\n", " no ip proxy-arp\n",
                               " no lldp transmit\n", "!\n"]
    return(l3_no_ip_xe_config_list)

def config_gen_ints_tun_xe(tun_xe_int):
    tun_xe_config_list = [tun_xe_int['label'] + "\n", " #this should be an XE tunnel interface\n",
                          " no ip unreachables\n", " no ip mask-reply\n", " no ip redirects\n",
                          " no ip proxy-arp\n", " no lldp transmit\n", "!\n"]
    return(tun_xe_config_list)

def config_gen_ints_tun_xr(tun_xr_int):
    tun_xr_config_list = [tun_xr_int['label'] + "\n", " #this should be an XR tunnel interface\n",
                          " no ip unreachables\n", " no ip mask-reply\n", " no ip redirects\n",
                          " no ip proxy-arp\n", " no lldp transmit\n", "!\n"]
    return(tun_xr_config_list)

def config_gen_ints_loop_xe(loop_xe_int):
    loop_xe_config_list = [loop_xe_int['label'] + "\n", " no ip directed-broadcast\n", " no ip unreachables\n",
                            " no ip mask-reply\n", " no ip redirects\n", " no ip proxy-arp\n", "!\n"]
    return(loop_xe_config_list)

def config_gen_ints_loop_xr(loop_xr_int):
    loop_xr_config_list = [loop_xr_int['label'] + "\n", " no ip directed-broadcast\n", " no ip unreachables\n",
                            " no ip mask-reply\n", " no ip redirects\n", " no ip proxy-arp\n", "!\n"]
    return(loop_xr_config_list)

def config_gen_ints(ints_to_gen, int_config_file):
    directory = "./configs/created/"
    int_config = open(directory + filename, 'w')
    int_config.writelines("!\n")
    for interface in interface_dict['interface_table']:
        if interface['type'] == "shut_xe":
            shut_xe_int_config = config_gen_shut_xe(interface)
            int_config.writelines(shut_xe_int_config)
        elif interface['type'] == "shut_xr":
            shut_xr_int_config = config_gen_shut_xr(interface)
            int_config.writelines(shut_xr_int_config)
        elif interface['type'] == "l2_access":
            l2_access_int_config = config_gen_l2_access(interface)
            int_config.writelines(l2_access_int_config)
        elif interface['type'] == "l2_dot1q":
            l2_dot1q_int_config = config_gen_l2_dot1q(interface)
            int_config.writelines(l2_dot1q_int_config)
        elif interface['type'] == "l3_vlan":
            vlan_l3_int_config = config_gen_ints_l3_vlan(interface)
            int_config.writelines(vlan_l3_int_config)
        elif interface['type'] == "l3_no_ip":
            l3_no_ip_xe_int_config = config_gen_ints_l3_no_ip_xe(interface)
            int_config.writelines(l3_no_ip_xe_int_config)
        elif interface['type'] == "tun_xe":
            tun_xe_int_config = config_gen_ints_tun_xe(interface)
            int_config.writelines(tun_xe_int_config)
        elif interface['type'] == "tun_xr":
            tun_xr_int_config = config_gen_ints_tun_xr(interface)
            int_config.writelines(tun_xr_int_config)
        elif interface['type'] == "loop_xe":
            loop_xe_int_config = config_gen_ints_loop_xe(interface)
            int_config.writelines(loop_xe_int_config)
        elif interface['type'] == "loop_xr":
            loop_xr_int_config = config_gen_ints_loop_xr(interface)
            int_config.writelines(loop_xr_int_config)
        elif interface['type'] == "l3_xe":
            xe_l3_int_config = config_gen_ints_xe_l3(interface)
            int_config.writelines(xe_l3_int_config)
        elif interface['type'] == "l3_xr":
            xr_l3_int_config = config_gen_ints_xr_l3(interface)
            int_config.writelines(xr_l3_int_config)
        else:
            print("Interface type " + interface['type'] + " not defined.")

directory = "./configs/source/"
for file in os.listdir(directory):
    interface_dict = {'interface_table': []}
    filename = file
    interface_config = ints_from_config(os.path.join(directory, file))
    config_gen_ints(interface_dict, filename)

#interface_config = ints_from_config('show_run_is02.txt')



# def lisp_int():
#     return(None)


save_results = open('interface_table.txt', 'w')
print(interface_dict, file=save_results)
print(interface_dict)