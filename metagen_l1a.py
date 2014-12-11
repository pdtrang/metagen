import csv
import sys
from cvxopt import *
from datetime import datetime
from l1 import l1

infile = sys.argv[1]
logfile = sys.argv[2]
outfile = sys.argv[3]

f1 = open(infile, "r")
reader = csv.reader(f1)

# g is number of genomes
g = 0
li = f1.readline()
g = len(li.split(",")) - 2
#print g

# n is number of k-mers
n = 0
for row in reader:
    n += 1
n = n + 1
#print n
f1.close()

f = open(infile, "r")
s1 = datetime.now()
F = matrix(0.0, (n, g))
b = matrix(0.0, (n, 1))
name = []

i = 0
for line in f.readlines():
    line = line.strip()
    #print(line)
    part = line.split(",")
    #print part 
    if (part[0] != "K-mer"):
        b[i,0] = float(part[len(part)-1])
    	for j in range(1,len(part)-1):
    		F[i,j-1] = float(part[j])
    	i = i + 1
    else:
        for idx in range(1,len(part)-1):
            name.append(part[idx])
    

s2 = datetime.now()
print "Read input: %s" %infile 

x, y = l1(F, b)
print "x = "
print x

out = open(outfile,'w')
if (len(x) > 0):
	for i in range(g):
		out.write("%s, %f\n" %(name[i],x[i,0]))
	out.close()
    
