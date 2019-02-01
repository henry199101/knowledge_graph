def print_file(file_name, end=''):
    for line in open(file_name):
        print(line, end=end)
