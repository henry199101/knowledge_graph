def make_a_list_of_strings(line, sep='\t'):
    import re

    if line[-1] == '\n':
        line = line[:-1]

    a_list_of_strings = re.split(sep, line)

    return a_list_of_strings


if __name__ == "__main__":
    line = "你好\t"
