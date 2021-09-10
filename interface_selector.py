import re
import os

#requests the Cisco configuration text file name
#file_name = input("File Name:")
#print(file_name)

def add_to_interface_dict(interface):
    interface_dict['interface_table'].append(interface)

def vlan_int(int_re_result_item):
    re_vlan_int = re.compile(r'interface Vlan.*', re.M).search(int_re_result_item)
    if re_vlan_int != None:
        interface = {}
        interface['label'] = re_vlan_int.group()
        interface['type'] = "L3"
        #            interface['location'] = "internal" "external"
        print(interface)
        add_to_interface_dict(interface)

def switch_int(int_re_result_item):
    print(int_re_result_item)
    re_swt_port = re.compile(r'^.switchport.*', re.M).search(int_re_result_item)
    if re_swt_port != None:
        re_port_label = re.compile(r'interface.*').match(int_re_result_item)
        interface = {}
        interface['label'] = re_port_label.group()
        interface['type'] = "L2"
    #            interface['location'] = "internal" "external"
        print(interface)
        add_to_interface_dict(interface)

def no_switch_int(int_re_result_item):
    print(int_re_result_item)
    re_no_swt_port = re.compile(r'^.no switchport.*', re.M).search(int_re_result_item)
    if re_no_swt_port != None:
        re_port_label = re.compile(r'interface.*').match(int_re_result_item)
        interface = {}
        interface['label'] = re_port_label.group()
        interface['type'] = "L3"
        #            interface['location'] = "internal" "external"
        print(interface)
        add_to_interface_dict(interface)

def loop_int(int_re_result_item):
    print(int_re_result_item)
    re_loop_int = re.compile(r'^interface Loopback.*', re.M).search(int_re_result_item)
    if re_loop_int != None:
        re_port_label = re.compile(r'interface.*').match(int_re_result_item)
        interface = {}
        interface['label'] = re_port_label.group()
        interface['type'] = "Loopback"
        #            interface['location'] = "internal" "external"
        print(interface)
        add_to_interface_dict(interface)

def tunnel_int(int_re_result_item):
    print(int_re_result_item)
    re_tunnel_int = re.compile(r'^interface Tunnel.*', re.M).search(int_re_result_item)
    if re_tunnel_int != None:
        re_port_label = re.compile(r'interface.*').match(int_re_result_item)
        interface = {}
        interface['label'] = re_port_label.group()
        interface['type'] = "Tunnel"
        #            interface['location'] = "internal" "external"
        print(interface)
        add_to_interface_dict(interface)

#Takes a Cisco config file and creates a file called re_results.txt with just the interface configs
def ints_from_config (config_file):
    file_open = open(config_file)
    print(file_open)
    #matches interface configuration sections
    re_get_ints = re.compile(r'(?<=!\n)(interface.*\n)(.*\n)*?(?=!)', re.M)
    read_config = file_open.read()
    execute_re = re_get_ints.finditer(read_config)
    for result in execute_re:
        result_value = result.group()
        switch_int(result_value)
        vlan_int(result_value)
        no_switch_int(result_value)
        loop_int(result_value)
        tunnel_int(result_value)

def config_gen_ints_l2 (l2_int):
    l2_config_list = [l2_int['label'] + "\n", "!\n"]
    return(l2_config_list)


def config_gen_ints_l3(l3_int):
    l3_config_list = [l3_int['label'] + "\n", " no ip directed-broadcast\n", " no ip unreachables\n", " no ip mask-reply\n", " no ip redirects\n", " no ip proxy-arp\n", " no lldp transmit\n", "!\n"]
    return(l3_config_list)

def config_gen_ints_tunnel(tunnel_int):
    tunnel_config_list = [tunnel_int['label'] + "\n", " no ip directed-broadcast\n", " no ip unreachables\n", " no ip mask-reply\n", " no ip redirects\n", " no ip proxy-arp\n", " no lldp transmit\n", "!\n"]
    return(tunnel_config_list)

def config_gen_ints_loopback(loopback_int):
    loopback_config_list = [loopback_int['label'] + "\n", " no ip directed-broadcast\n", " no ip unreachables\n", " no ip mask-reply\n", " no ip redirects\n", " no ip proxy-arp\n", "!\n"]
    return(loopback_config_list)

def config_gen_ints(ints_to_gen, int_config_file):
    directory = "/home/tcrowe/shares/iCloud Drive/Ansible/cml/STIG_Automation/temp/stig_int_config/"
    int_config = open(directory + filename, 'w')
    int_config.writelines("!\n")
    for interface in interface_dict['interface_table']:
        if interface['type'] == "L2":
            l2_int_config = config_gen_ints_l2(interface)
            int_config.writelines(l2_int_config)
        elif interface['type'] == "L3":
            l3_int_config = config_gen_ints_l3(interface)
            int_config.writelines(l3_int_config)
        elif interface['type'] == "Tunnel":
            tunnel_int_config = config_gen_ints_tunnel(interface)
            int_config.writelines(tunnel_int_config)
        elif interface['type'] == "Loopback":
            loopback_int_config = config_gen_ints_loopback(interface)
            int_config.writelines(loopback_int_config)
        else:
            print("Interface type " + interface['type'] + " not defined.")

directory = "/home/tcrowe/shares/iCloud Drive/Ansible/cml/STIG_Automation/temp/backups"
for file in os.listdir(directory):
    interface_dict = {'interface_table': []}
    filename = file
    interface_config = ints_from_config(os.path.join(directory, file))
    config_gen_ints(interface_dict, filename)

#interface_config = ints_from_config('show_run_is02.txt')



def lisp_int():
    return(None)


save_results = open('interface_table.txt', 'w')
print(interface_dict, file=save_results)
print(interface_dict)