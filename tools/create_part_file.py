def create_part_of_a_file(source_file, number, destiny_file):
	with open(destiny_file, 'w') as destiny:
		count = 0
		for line in open(source_file):
			count += 1
			if count >= number:
				break
			destiny.write(line)


if __name__ == '__main__':
	source_file = 'files/baiketriples.txt'

	number_of_one_thousandth_of_source_file = 65000
	number = 10 * number_of_one_thousandth_of_source_file

	destiny_file = 'files/baiketriples_1_to_100.txt'

	create_part_of_a_file(source_file, number, destiny_file)
