## Script to calculate binding energies of all possible mutations 
## at the interface of a protein with a target (another protein or ligand)

## Usage: python calculate_binding.py inputpdb.pdb

## proteinchain and ligandchain below allow you to alter which chain of the pdb is protein vs ligand
## residuedistance is the distance in angstroms around the ligand you want to mutate

### If you are using parameters for a ligand or molecule that isnt natively recognised by FoldX
### You need to enable the commented lines 80-83, and change the name to that of the ligand file
### This will allow FoldX to copy the file into the correct locations

import Bio.PDB
import os
import shutil
import sys

proteinchain = "A"
ligandchain = "C"
foldxdir = "~/Foldx_location"
residuedistance = 10




parser = Bio.PDB.PDBParser(QUIET=True)

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

aalist = ["A", "R", "N", "D", "C", "E", "Q", "G", "H", "I", "L", "K", 
"M", "F", "P", "S", "T", "W", "Y", "V"]

pdbfile = sys.argv[1]


structure = parser.get_structure('', pdbfile)

atoms  = Bio.PDB.Selection.unfold_entities(structure[0], proteinchain)

ns = Bio.PDB.NeighborSearch(atoms)

ligand = structure[0][ligandchain].get_atoms()

residuelist = []
for atom in ligand:
    close_atoms = ns.search(atom.coord, residuedistance, level="R")
    for residue in close_atoms:
        if residue.get_full_id()[2] == proteinchain:
            restype = residue.get_resname()
            resid = residue.id[1]
	    residuelist.append((restype, resid))
	
residues_nearby = (list(set(residuelist)))

count= 1
for residue in residues_nearby:
    res_folder = "residue_" + str(residue[1])
    if not os.path.exists(res_folder):
        os.makedirs(res_folder)
    else:
        print("Ignoring " + res_folder + " as it already exists")
	continue
    os.chdir(res_folder)
    shutil.copyfile("../" + pdbfile, "./pdbfile.pdb")


## Code for copying non-standard molecules (see other code for how to generate these files for molecules)    
#    if not os.path.exists("./molecules"):
#        os.makedirs("./molecules")
#    shutil.copyfile("../3JD.json", "./molecules/3JD.json")
    
    residue_code= threetoone(residue[0])
    
    mutation_list = []
    
    for aa in aalist:
	if aa == residue_code:
	    continue
        else:
            mutantcode = residue_code + proteinchain + str(residue[1]) + aa
	    mutation_list.append(mutantcode)
	   
    for item in (mutation_list):
        with open("individual_list_" + item + ".txt", "w") as text_file:
	    text_file.write(item + ";")
        buildmodel = foldxdir + "/foldx --command=BuildModel --pdb=pdbfile.pdb --numberOfRuns=1 --pH=7 --vdwDesign=2 --ionStrength=0.05 --water=CRYSTAL --mutant-file=individual_list_" + item + ".txt"
        os.system(buildmodel)
	os.rename("WT_pdbfile_1.pdb", item + "_WT_pdbfile.pdb")
	os.rename("pdbfile_1.pdb", item + "_MUT_pdbfile.pdb")
	
	analysecomplex_WT = foldxdir + "/foldx --command=AnalyseComplex --pdb=" + item + "_WT_pdbfile.pdb --analyseComplexChains=" + proteinchain + "," + ligandchain + " --pH=7 --vdwDesign=2 --ionStrength=0.05 --water=CRYSTAL"	    	    
        os.system(analysecomplex_WT)
	analysecomplex_MUT = foldxdir + "/foldx --command=AnalyseComplex --pdb=" + item + "_MUT_pdbfile.pdb --analyseComplexChains=" + proteinchain + "," + ligandchain  + " --pH=7 --vdwDesign=2 --ionStrength=0.05 --water=CRYSTAL"
        os.system(analysecomplex_MUT)
    os.chdir("../")


print("#####################")   
print("Calculations Complete")
print("#####################")   
