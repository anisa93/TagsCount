import csv
import os
def read_file_with_relative_path(file_name):
    current_directory = os.getcwd()
    relative_path = os.path.join(current_directory, file_name)
    if not os.path.exists(relative_path):
        raise FileNotFoundError(f"The file {relative_path} does not exist.")
    return relative_path
def read_flow_logs():
    data = []
    file_name = 'flow_data.txt'
    relative_path = read_file_with_relative_path(file_name)
    with open(relative_path, 'r') as data_file:
        flow_data = data_file.readlines()
        field_names = flow_data[0].strip()
        for line in flow_data[1:]:
            data.append(line.rstrip())
    return data
def read_lookup_file():
    lookup_data = []
    file_name = 'tag_data.txt'
    relative_path = read_file_with_relative_path(file_name)
    with open(relative_path, 'r') as lookup_file:
        csv_reader = csv.reader(lookup_file)
        next(csv_reader)
        for row in csv_reader:
            if row and any(field.strip() for field in row):
                lookup_data.append(','.join(field.strip() for field in row))
    return lookup_data
def lookup_map_creation(a):
    lookup_map = {}
    for l in a:
        row = l.split(",")
        t = (row[0], row[1])
        v = row[2]
        if t not in lookup_map:
            lookup_map[t] = v
    return lookup_map
def solution():
    lookup_map = lookup_map_creation(read_lookup_file())
    tag_count = {}
    tag_count["untagged"] = 0
    protocol_count = {}
    flow_input = read_flow_logs()
    for i in flow_input:
        row = i.split(" ")
        lookup_key = (row[10], row[6])
        if lookup_key not in lookup_map:
            tag_count["untagged"] += 1
        else :
            v = lookup_map[lookup_key]
            if v not in tag_count:
                tag_count[v] = 1
            else:
                tag_count[v] += 1 
        if lookup_key not in protocol_count:
            protocol_count[lookup_key] = 1
        else:
            protocol_count[lookup_key] += 1
    relative_path = read_file_with_relative_path('output.txt')
    with open(relative_path, 'w') as file:
        file.write("tags, count\n")
        for tag, count in tag_count.items():
            file.write(f"{tag}, {count}\n")
        file.write("\n")
        file.write("port, protocol, count\n")
        for (port, protocol), count in protocol_count.items():
            file.write(f"{port}, {protocol}, {count}\n")
solution()