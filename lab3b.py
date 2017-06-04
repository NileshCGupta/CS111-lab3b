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
i_first_free = superblock[7]

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
		datablocks[inode] = i_datablocks
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

# print(actuallinkscount)
f.close()
