import random as rd
from copy import deepcopy
from math import sqrt
import numpy as np
import time
import json

"""Overall idea: 
1. Create a list Pop with MaxPopSize initial solutions
- Each solution contains of M route of salesmen.
- Updated solution created by removing some nodes from list of nodes, then re-insert it in random route by function *insert* in order to find a better solution.
- Sorting Pop by worst cost of each solution with function *PopSorted*.
2. From Pop, keep (size(Pop)/f) best solutions from Pop
- f is a value that we decided. 
I.e: f = 2, MaxPopSize = 100 then keep 50 best solutions.
3. From each remaining solutions, perform it with LNS algorithm to find even better solution
- LNS: Perform (nofmutations) mutations by removing some random nodes from solutions then re-insert it in the solution again, if it's better update this solution as new solution.
- Two different ways to remove nodes: 

If the problem is m-ATSP (general case) then we use function *RmvR*, pick a random number of nodes from alp.N to beta.N.

If the problem is m-ATSP (direct case) then we use function *RmvP*, pick some seeds from N, then choose some nodes nearest to each seed and remove from solution, include seed itself, total number of remove nodes is random from alp.sqrt(N) to beta.sqrt(N), since it's more targerted.

alp and beta are values we decide.
4. We start with an initial number of mutations which we decide, then after each iteration, while the size of Pop decrease, we also increase the number of mutations.
5. When the size of Pop go below MinPopSize, return the best solution from remaning solutions in Pop.
"""
# print solution
def printSolution(sol):
    for i in range(len(sol)):
        print("Salesman %d: "%(i+1), end = " ")
        for j in sol[i][:-2]:
            print("%d"%j, end=" -> ")
        print(0)
        print("Path cost: %d"%(sol[i][-1]))
        print()
    return 

#return the worst cost of a solution
def worstCost(cr,c):                  
    wc = -1
    for path in cr:
        cost = 0
        for i in range(len(path)-2):
            cost += c[path[i]][path[i+1]]
        if cost > wc:
            wc = cost
    return wc

#the cost of a route 
def cost(route, c):
    cost = 0
    for i in range(len(route)-2):
        cost += c[route[i]][route[i+1]]
    return cost

"""Algorithm 1: Remove a node from route then re-insert again."""

#algorithm 1: NodeInsert
def rmvNodeRandom(nodes):             
    rmvPos = rd.randint(0, len(nodes)-1)
    rmvNode = nodes.pop(rmvPos)
    return rmvNode

def addNode(route, i, n_j):             
    r_ = deepcopy(route)
    r_.insert(i+1, n_j)
    return r_

def insert(sol, nodes, c):      
    while len(nodes) != 0:
        minwcost = 1e20   
        n_j = rmvNodeRandom(nodes)                   
        for r in sol:                             
            for i in range(len(r)-2):
                rP = addNode(r, i, n_j)
                cost_rP = cost(rP, c)
                if cost_rP < minwcost:
                    rP[-1] = cost_rP
                    bestr, bestrP = deepcopy(r), deepcopy(rP)
                    minwcost = cost_rP
        sol.remove(bestr)
        sol.append(bestrP)
        sol.sort(key=lambda x: x[-1])
    return sol
#end algorithm 1

"""Algorithm 2: Remove k random nodes from a solution.
- RmvR: Use for general case
- RmvP: Use for direct case
"""

#algorithm 2: NodeRemoval - 2 strategy (m-ATSP, m-TSP)
def pickRandom(N, nofnodes):
    return rd.sample(N, nofnodes)

def rmvNode(cur, n):
    for i in cur:
        if n in i[1:-2]:
            i.remove(n)
            break

def nearestNode(s, nofnodesP, c):      #use for problem 2
    s_ = []
    for i in range(1, len(c[s])):
        s_.append([c[s][i], i])
    sorted(s_)
    sn = []
    for i in range(nofnodesP):
        sn.append(s_[i][1])
    return sn    

#first method use for m-ATSP
def RmvR(sol, nofnodes, N):       #change the original solution
    free = pickRandom(N, nofnodes) 
    for n in free:
        rmvNode(sol,n)
    return sol, free
#end method

#second method use for m-TSP
def RmvP(sol, nofnodes, nofseeds, N, c):  #change the original solution 
    nofnodesP = int(nofnodes/nofseeds)
    seeds = pickRandom(N, nofseeds) 
    free = []
    for s in seeds:
        nn = nearestNode(s, nofnodesP, c) #include s itself
        for n in nn:
            rmvNode(sol, n)
            free.append(n)
    return sol, free
#end method

#end algorithm 2

"""Algorithm 3: Large neighbor search - mutating some random nodes using algo 2 then re-insert it with algo 1.

"""

#algorithm 3: LNS
def LNS(sol, nofmutations, rmvopt, alp, beta, N, c, n):
    if rmvopt == "rand":
        lower, upper = int(alp*n), int(beta*n)
    if rmvopt == "proximity":
        lower, upper = int(alp*sqrt(n)), int(beta*sqrt(n))

    wc = sol[-1][-1]

    for i in range(nofmutations):
        rmv = rd.randint(lower, upper)
        if rmvopt == "rand":
            tmp, free = RmvR(deepcopy(sol), rmv, N)
        elif rmvopt == "proximity":
            seeds = rd.randint(1, int(upper/10))
            tmp, free = RmvP(deepcopy(sol), rmv, seeds, N, c)
        for i in tmp:
            i[-1] = cost(i, c)
            
        tmp.sort(key=lambda x: x[-1])
        new_sol = insert(tmp, free, c)
        newwc = new_sol[-1][-1] 

        if newwc <= wc:
            wc = newwc
            sol = deepcopy(new_sol)
    return sol
#end function

"""Algorithm 4: Main algorithm 
- Build MaxPopSize initial soutions, then select nofsol/f fittest solutions to keep with f is a given value.
- Each solution in remaining solutions goes through algo 3 to find even better result.
- When only MinPopSize solutions left, pick the fittest solution. 
"""

#algorithm 4: TS-LNS - Main algorithm
def initLNSMutations():           #simple version
    return 100

def adjustLNSMutations(mut):      #simple version
    return mut + 100

def getFittest(Pop, nofsol_kept): 
    return Pop[:nofsol_kept]


def TS_LNS(N, M, rmvopt, MaxPopSize, MinPopSize, cmb, f, alp, beta, c, n):
    nullsol = []
    Pop = list()
    
    for i in range(M):
        nullsol += [[0, 0, 0]]

    for i in range(MaxPopSize):
        P = deepcopy(N)
        Pop.append(insert(deepcopy(nullsol), P, c))

    Pop.sort(key=lambda x: x[-1][-1])           
    
    
    if cmb == "YES":
        print("Solution of TS: ", Pop[0])
        print()
        print("Solution of LNS: ")
        mut = initLNSMutations()    
        while len(Pop) > MinPopSize:
            Pop = getFittest(Pop, int(len(Pop)/f))         
            for sol in Pop:
                sol = LNS(sol, mut, rmvopt, alp, beta, N, c, n)
            Pop.sort(key=lambda x: x[-1][-1])
            mut = adjustLNSMutations(mut)              

    return getFittest(Pop, 1)[0]
#end function

"""Random datasets generator

"""

def gena(N0, K0):
    d = [0]
    for i in range(N0):
        d.append(rd.randint(1, 100))
    
    t = []
    for i in range(N0+1):
        row = []
        for j in range(N0+1):
            if i == j:
                row.append(0)
            else:
                row.append(rd.randint(1,100))
        t.append(row)
    c = np.array(t) + np.array(d)
    c = c.tolist()
    
    for i in range(len(c)):
        c[i][i] = 0

    return t, d, c
def gens(N0, K0):
  c = [[0 for i in range(N0+1)] for j in range(N0+1)]
  for i in range(N0+1):
    for j in range(N0+1):
      if i != j:
        point = rd.randint(1, 100)
        c[i][j], c[j][i] = point, point
  return c

"""Datasets lib"""

def datasets(filename):
    with open(filename) as f:
        N, M = [int(i) for i in f.readline().split()]
        d = [0] + [int(i) for i in f.readline().split()]
        t = []
        for i in range(N+1):
            arr = [int(i) for i in f.readline().split()]
            t.append(arr)
        c = np.array(t) + np.array(d)
        c = c.tolist()
        for i in range(len(c)):
            c[i][i] = 0
        return N, M, d, t, c

# if __name__ == "__main__":
#     case = input("mATSP / mTSP (1/2): ")
#     combine = input("Combine with LNS:(YES/NO) ")
#     if case == "1":
#         n, M = int(input("Number of customers: ")), int(input("Number of salesmen: "))
#         t, d, c = gena(n, M)
#         rmvopt = "rand"
#         alp = .2
#         beta = .4
#         # print("Time table for going from point to point: ", end = " ")
#         # print(np.array(t))
#         # print("Time for customers: ", end = " ")
#         # print(np.array(d))
#     else:
#         # filename = input("Choose a datasets file: ")
#         # N, M, d, t, c = datasets(filename)
#         n, M = int(input("Number of customers: ")), int(input("Number of salesmen: "))
#         c = gens(n, M)
#         rmvopt = "proximity"
#         alp = 1
#         beta = 4
#         # print(np.array(c))

#     N = [i+1 for i in range(n)]
#     node0 = 0
#     MaxPopSize = 100
#     MinPopSize = 6    
#     f = 2
#     sol = TS_LNS(N, M, rmvopt, node0, MaxPopSize, MinPopSize, combine, f, alp, beta, c, n)
#     for i in sol:
#         print(i)
#     print(worstCost(sol, c))

#datasets
with open('D:\Programming\Optimization\mini project\my project\datasets\sample05.json', 'r') as f:
	input1 = json.load(f)
n, M, d, t = input1['N'], input1['k'], input1['d'], input1['t']
N = []
for i in range(n):
    N.append(i+1)
c = np.array(t) + np.array(d)
for i in range(c.shape[0]):
    c[i][i] = 0
c = c.tolist()
node0 = 0

# rmvopt, MaxPopSize, MinPopSize, cmb, f, alp, beta = input("m-TASP(rand)/m-TSP(proximity): "), int(input("Max solution: ")), int(input("Min solution: ")), input("Combine with LNS (YES/NO): "), int(input("Decrement factor: ")), float(input("lower bound: ")), float(input("upper bound: "))
rmvopt, MaxPopSize, MinPopSize, cmb, f, alp, beta = "rand", 100, 6, "YES", 2, 0.2, 0.4
print("running ...")

#running algorithm
start = time.time()
sol = TS_LNS(N, M, rmvopt, MaxPopSize, MinPopSize, cmb, f, alp, beta, c, n)
end = time.time()

#print solution
printSolution(sol)

#print the slowest path
print("Worst cost: %d"%worstCost(sol, c)) 
print("Running time: %.8f"%(end-start))       


