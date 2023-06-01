import sys,os, shutil

pdbfile = sys.argv[1]
repairnumber = 10
foldx_location = "~/Foldx"
pdbfile_base = pdbfile.split(".")[0]

# do first repair
foldx_repair1 = foldx_location + "/foldx --command=RepairPDB --pdb=" + pdbfile + " --water=CRYSTAL"
os.system(foldx_repair1) 

for i in range(0,repairnumber-1):
    foldx_repair2 = foldx_location + "/foldx --command=RepairPDB --pdb=" + pdbfile_base + "_Repair.pdb --water=CRYSTAL"
    os.system(foldx_repair2)
    shutil.copy(pdbfile_base + "_Repair_Repair.pdb", pdbfile_base + "_Repair.pdb")

shutil.copy(pdbfile_base + "_Repair_Repair.pdb", pdbfile_base + "_Repair_final.pdb")
os.remove(pdbfile_base + "_Repair_Repair.pdb")
os.remove(pdbfile_base + "_Repair.pdb")

