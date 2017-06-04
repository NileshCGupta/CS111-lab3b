#!/usr/bin/python

import sys

print('Number of arguments:', len(sys.argv), 'arguments.')

filename = sys.argv[1]
f = open(filename, 'r')

bfree = []
ifree = []
inodes = []

for line in f:
	if line.startswith("BFREE"):
		bfree.append(line[6:].rstrip())
	if line.startswith("IFREE"):
		ifree.append(line[6:])
	if line.startswith("INODE"):
		inodes.append(line[6:line.index(',')])

print(bfree)
print(ifree)

superblock = f.readline()
groupinfo = f.readline()

f.close()
