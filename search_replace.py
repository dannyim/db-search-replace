#!/usr/bin/python
import argparse
import re
import datetime


def search_replace(f, search, replace):
	regex = r's:([\d]+):'
	t = datetime.datetime.now()
	fname = f.name
	datestr = t.strftime('%Y-%m-%d-T%H-%M-%S')
	newfile_name = '%s_%s' % (datestr, fname)
	with open(newfile_name, 'wb') as newfile:
		for line in f:
			newline = line
			# find serialized strings in the current line
			# and replace, updating the length
			for m in re.finditer(regex, line):
				s = m.start()
				e = m.end()
				length = int(m.group(1))
				# add 2 to account for double quotes
				substr = line[e:e+length + 2]
				# ensure that it is a valid serialized string before replacing
				if substr[0] == '"' and substr[-1] == '"':
					stripped_substr = substr[1:-1]
					if search in stripped_substr:
						newstr = stripped_substr.replace(search, replace)
						newlen = len(newstr)
						# replace the line with new contents
						beg = line[:s]
						serialstart = "s:%d:" % newlen
						mid = serialstart + newstr
						end = line[e+length+2:]
						newline = beg + mid + end
			# search and replace non-serialized occurences of the search string
			newline = newline.replace(search, replace)
			newfile.write(newline)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description=("Search and replace without corrupting php "
			"serialized strings"),
		epilog=("A file is created in the current directory prefixing "
			"the current datetime to the original filename")
		)
	parser.add_argument("file",
		type=file,
		help="The file to modify")
	parser.add_argument('search', help="The string to replace")
	parser.add_argument('replace', help="The replacement string")
	args = parser.parse_args()
	db_file = args.file
	search = args.search
	replace = args.replace
	search_replace(db_file, search, replace)
