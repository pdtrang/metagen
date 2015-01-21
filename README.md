metagen
=======
Goal: Use linear programming, linear equation, l1-approximation to estimate abundance.

How to run:

Require Python 2.7.6

Input: 
- csv file: frequencies of k-mer in Microbial genomes and in Reads

Output:
- logfile.txt: contains running time of each step.
- sol.csv: solution for variables x_1, x_2,...,xm (and y_1,y_2,....y_n)

1. metagen_lp.py
  - Linear programming: Find x and minimal value of y_1+y_2+....+y_n for which Fx+y=b. x is the abundance of the genomes in the sample, y is the abundance of other unknown genomes.
  - Require Gurobi installation at least version 5.6.3 (http://www.gurobi.com/)
  - Command: python metagen_lp.py inputfile.csv logfile.txt sol.csv

2. metagen_le.py
  - Linear equation: solve for x in Fx=b
  - Require Gurobi installation at least version 5.6.3 (http://www.gurobi.com/)
  - Command: python metagen_le.py inputfile.csv logfile.txt sol.csv

3. metagen_l1a.py
  - L1-approximation: find x to minimize |Fx-b|
  - Require CVXOPT 1.1.7 (http://cvxopt.org/).
  - metagen_l1a.py calls the function l1(P, q) (http://cvxopt.org/examples/mlbook/l1.html)
  - Command: python metagen_l1a.py inputfile.csv logfile.txt sol.csv
