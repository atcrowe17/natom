import re
import os


# requests the Cisco configuration text file name
# file_name = input("File Name:")

# Takes a Cisco config file and creates a file with just the interface configurations
def ints_from_config(config_file, filename):
    file_open = open(config_file)
    print(file_open)
    # matches interface configuration sections
    re_get_ints = re.compile(r'(?<=!\n)(interface.*\n)(.*\n)*?(?=!)', re.M)
    read_config = file_open.read()
    execute_re = re_get_ints.finditer(read_config)
    file_open.close()
    parsed_configs = []
    parsed_directory = "/home/xargenius/Desktop/iCloud_to_Linux_Share/xe_config_compare/parsed_results/"
    parsed_file = open(parsed_directory + "ints_" + filename, "w")
    parsed_file.write("!\n")
    for result in execute_re:
        result_value = result.group()
        parsed_configs.append(result_value+"!\n")
    parsed_file.writelines(parsed_configs)


def compare_ints (parsed_file1, parsed_file2):
    parsed_files = [parsed_file1,parsed_file2]
    re_get_ints = re.compile(r'(?<=!\n)(interface.*\n)(.*\n)*?(?=!)', re.M)
    for file in parsed_files:
        file_open = open(file)
        read_file = file.read()
        execute_re = re_get_ints.finditer(read_file)

comparefile_1 = ("/home/xargenius/Desktop/iCloud_to_Linux_Share/xe_config_compare/testconfigs/sdni-ub1-is-02_config")
file_open = open(comparefile_1)
# matches interface configuration sections
re_get_ints = re.compile(r'(?<=!\n)([^!].*\n)(.*\n)*?(?=!)', re.M)
read_config = file_open.read()
execute_re = re_get_ints.finditer(read_config)
file_open.close()
parsed_configs = []
parsed_directory = "/home/xargenius/Desktop/iCloud_to_Linux_Share/xe_config_compare/parsed_results/"
parsed_file = open(parsed_directory + "regex_results", "w")
parsed_file.write("#####  NEW SECTION #####\n")
for result in execute_re:
    result_value = result.group()
    parsed_configs.append(result_value + "#####  NEW SECTION #####\n")
parsed_file.writelines(parsed_configs)

# comparefile_2 = open("/home/xargenius/Desktop/iCloud_to_Linux_Share/xe_config_compare/testconfigs/sdni-ub1-is-02-as-is-run.txt")


def compare_single_line(file_1, file_2):
    read_file_1 = file_1.readlines()
    read_file_2 = file_2.readlines()
    re_find_ex = re.compile(r'^!.*', re.M)
    compare_results_list = []
    results_directory = "/home/xargenius/Desktop/iCloud_to_Linux_Share/xe_config_compare/parsed_results/"
    compare_results_file = open(results_directory + "is-02-compare", "w")
    for line in read_file_1:
        if re_find_ex.match(line):
            continue
        if line in read_file_2:
            compare_results_list.append("yes: " + line)
        else:
            compare_results_list.append("no: " + line)
    compare_results_file.writelines(compare_results_list)
    compare_results_file.close()






# directory = "/home/xargenius/Desktop/iCloud_to_Linux_Share/xe_config_compare/testconfigs"
# for file in os.listdir(directory):
#     filename = file
#     ints_from_config(os.path.join(directory, file), filename)
