import sys,os

d = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
     
def threetoone(x):
    if len(x) % 3 != 0: 
        raise ValueError('Input length should be a multiple of three')

    y = ''
    for i in range(len(x) // 3):
            y += d[x[3 * i : 3 * i + 3]]
    return y


pdbfile = sys.argv[1]
foldx_location = "~/Foldx/"
residuelist = []
with open(pdbfile, 'r') as f:
    for a in f:
        if a.startswith("#"):
	    continue
	elif a.startswith("TER"):
	    continue
	else:
	    pdbline = ([a[12:16].strip(), a[17:20].strip(), int(a[22:26]), a[21],
            float(a[30:38]), float(a[38:46]), float(a[46:54])])
	    
	    if pdbline[1] in ["GTP", "MG"]:
	        continue
	    else:
	        residuelist.append(threetoone(pdbline[1]) + pdbline[3] + str(pdbline[2]) + "a")
residuelist = set(residuelist)

foldx_positionscan = foldx_location +"foldx --command=PositionScan --pdb=" +pdbfile + " --position=" + ",".join(residuelist)
os.system(foldx_positionscan)

