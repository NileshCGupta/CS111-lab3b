#!/usr/bin/python

import sys

filename = sys.argv[1]
f = open(filename, 'r')

bfree = []
ifree = []
inodes = [] #List of all inodes
directoryInodes = [] #List of all DIRECTORY inodes
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
		inodes.append(inode)
		linkscount = curline[6]
		i_datablocks = curline[12:24]
		#print(i_datablocks)
		datablocks[inode] = i_datablocks
		givenlinkscount[inode] = linkscount
		if int(inode) < int(i_first_free):
			reservedblocks.extend(i_datablocks)
			#directoryInodes.append(inode) 
		if curline[2] == 'd':
			directoryInodes.append(inode)

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

#To remove 0 data blocks that may occur in reserved blocks
while '0' in reservedblocks: 
	reservedblocks.remove('0')

for x in inodes:
	while '0' in datablocks[x]:
		datablocks[x].remove('0')


# print(actuallinkscount)
#Some debugging information to make sure we have all the data we need

#Free blocks
for x in bfree:
	print("Free block: ", x)
print('\n')

#Free inodes
for x in ifree:
	print("Free inode: ", x)
print('\n')

#Reserved data blocks
for x in reservedblocks:
	print("Reserved block: ", x)
print('\n')

for x in inodes:
	print("Inode number: ", x)
	print("Inode uses these data blocks: ", datablocks[x])
	print("Inode ", x, " supposedly has ", givenlinkscount[x], "links in filesystem")
	print("Inode ", x, " actually has ", actuallinkscount[x], "links in filesystem")
	print("\n")

for x in directoryInodes:
	print("Directory inode number: ", x)
	print("Directory inode", x, " uses these data blocks: ", datablocks[x])
	print("Directory inode", x, " has entries pointing to these inodes: ", dirents[x])
	print("\n")



f.close()
