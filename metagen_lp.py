import csv
import sys
from gurobipy import *
from datetime import datetime

infile = sys.argv[1]
logfile = sys.argv[2]
outfile = sys.argv[3]

f = open(infile, "r")

F = {}
b = []
name = []

# n is number of k-mers
s1 = datetime.now()
n = 0
for line in f.readlines():
    line = line.strip()
    #print(line)
    part = line.split(",")
    #print part
    if (part[0] != "K-mer"):
        b.append(float(part[len(part)-1]))
        for j in range(1,len(part)-1):
        	F[n,j-1] = float(part[j])
        n = n + 1
    else:
        for idx in range(1,len(part)-1):
            name.append(part[idx])

# g is number of genomes
g = len(part) - 2

s2 = datetime.now()
print "Read input: %s" %infile 

try:
	print "Building model......"
	s3 = datetime.now()
	m = Model("metagen_lp")

	# Variables
	x = [None] * (g)
	y = [None] * (n)
	for i in range(g):
		x[i] = m.addVar(lb = 0, vtype = GRB.CONTINUOUS, name=name[i])
        for i in range(n):
		y[i] = m.addVar(lb = 0, vtype = GRB.CONTINUOUS, name="y"+str(i))
	
	m.update()

	# Objective
	obj = LinExpr()	
	for i in range(n):
		obj += y[i]
	
	m.setObjective(obj, GRB.MINIMIZE)

	# Constraints
	for i in range(n):
		constr = LinExpr()
		for j in range(g):
                    constr += F[i,j] * x[j]
                    
                m.addConstr(constr + y[i] == b[i])
		
	print "Finish building model"
	s4 = datetime.now()
	print s4 - s3

	s5 = datetime.now()
        print "\n"
	m.optimize()
        
        if m.SolCount > 0:
            for v in m.getVars():
    	       print('%s %f' %(v.varName, v.x))

            print ('Obj: %g' %m.objVal)
        else:
            print "No solution found."

        s6 = datetime.now()

        if m.SolCount > 0:
            out = open(outfile,'w')
            for v in m.getVars():    	
                out.write('%s, %f \n' %(v.varName, float(v.x)))
            out.close()

        log = open(logfile,'w')
        log.write("Number of genomes = %d\n" %g)
        log.write("Number of k-mers = %d\n" %n)
        log.write("Read input = " + str(s2 - s1) + "\n")
        log.write("Build model = " + str(s4 - s3) + "\n")
        log.write("Solve LP = " + str(s4 - s3))
        log.close()

except GurobiError as e:
	print('Error reported')
        print e.errno
