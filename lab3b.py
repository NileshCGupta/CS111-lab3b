#!/usr/bin/python

import sys

filename = sys.argv[1]
f = open(filename, 'r')

bfree = []
ifree = []
inodes = []
reservedblocks = []
datablocks = {}
dirents = {}
givenlinkscount = {}
actuallinkscount = {}

# datablocks = {inode, [[datablocks], given links count, actual links count]}

superblock = f.readline().split(',')
num_blocks = int(superblock[1])
i_first_free = int(superblock[7])

for line in f:
	if line.startswith("BFREE"):
		bfree.append(line[6:].rstrip())

	if line.startswith("IFREE"):
		ifree.append(line[6:].rstrip())

	if line.startswith("INODE"):
		curline = line.split(',')
		inode = curline[1]
		linkscount = curline[6]
		i_datablocks = curline[12:24]
		datablocks[inode] = []
		for i in range(0, 12):
			tup = (curline[12+i], '0')
			datablocks[inode].append(tup)

		givenlinkscount[inode] = linkscount
		if int(inode) < int(i_first_free):
			reservedblocks.extend(i_datablocks)

	if line.startswith("DIRENT"):
		curline = line.split(',')
		inode = curline[1]
		i_dirent = curline[3]
		# add entry to directory data
		if inode in dirents:
			dirents[inode].append(i_dirent)
		else:
			dirents[inode] = [i_dirent]
		# add reference count for entry
		if i_dirent in actuallinkscount:
			actuallinkscount[i_dirent] += 1
		else:
			actuallinkscount[i_dirent] = 1

	if line.startswith("INDIRECT"):
		curline = line.split(',')
		inode = curline[1]
		level = curline[2]
		blocknum = curline[5].rstrip()
		tup = (blocknum, level)
		datablocks[inode].append(tup)

while '0' in reservedblocks:
	reservedblocks.remove('0')

for key in datablocks:
	while ('0', '0') in datablocks[key]:
		datablocks[key].remove(('0', '0'))

level = { 	0: "", 
			1: "INDIRECT", 
			2: "DOUBLE INDIRECT", 
			3: "TRIPLE INDIRECT" }
			
all_datablocks = []

for key in datablocks:
	for value in datablocks[key]:
		#print(int(value))
		if int(value[0]) > num_blocks:
			print("INVALID ", level[int(value[1])], " BLOCK ", value, " IN INODE ", key, " AT OFFSET ", datablocks[key].index(value), "\n")

		if int(key) > i_first_free:
			if int(value[0]) < i_first_free:
				print("RESERVED ", level[int(value[1])], " BLOCK ", value, " IN INODE ", key, " AT OFFSET ", datablocks[key].index(value), "\n")

		if value[0] in bfree:
			print("ALLOCATED ", level[int(value[1])], " BLOCK ", value, " ON FREELIST\n")

		if value[0] in all_datablocks:
			print("DUPLICATE ", level[int(value[1])], " BLOCK IN INODE ", value, " AT OFFSET ", datablocks[key].index(value), "\n")
		else:
			all_datablocks.append(int(value[0]))

print(datablocks)



f.close()
