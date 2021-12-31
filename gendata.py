#asymmetric case
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
    return t, d

if __name__ == "__main__":
    t, d = gena(n, k)
    dict = {'N': n,
			'k': k,
			'd': d.tolist(),
			't': t.tolist()}
    with open(filename, 'w') as f:
      json.dump(dict, f, indent=3)
