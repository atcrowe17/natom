import re
import os

#requests the Cisco configuration text file name
file_name = input("File Name:")

#Takes a Cisco config file and creates a file called re_results.txt with just the interface configs
def ints_from_config (config_file):
    file_open = open(config_file)
    print(file_open)
    #matches interface configuration sections
    re_get_ints = re.compile(r'(?<=!\n)(interface.*\n)(.*\n)*?(?=!)', re.M)
    read_config = file_open.read()
    execute_re = re_get_ints.finditer(read_config)

directory = "/home/tcrowe/shares/iCloud Drive/Ansible/cml/STIG_Automation/temp/backups"
for file in os.listdir(directory):
    interface_dict = {'interface_table': []}
    filename = file
    interface_config = ints_from_config(os.path.join(directory, filename))
    config_gen_ints(interface_dict, filename)