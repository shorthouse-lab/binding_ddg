## This script summarises the results from the binding_ddg.py calculations. Run this script in the directory containing
## the folders from binding_ddg.py

# Useage: python summary_binding_ddg.py

import os, sys
import glob
import pandas as pd


ddg_list = []
ddg_list.append(["Mutation", "WT_energy", "MUT_energy", "DDG"])
for item in glob.glob("./residue*"):
    os.chdir(item)
    for item in glob.glob("./*_MUT_pdbfile.pdb"):
        mutation = item.split("_")[0].split("/")[1]
	wtfile = "Summary_" + mutation + "_WT_pdbfile_AC.fxout"
	mutfile = "Summary_" + mutation + "_MUT_pdbfile_AC.fxout"
	
	wt_array = pd.read_csv(wtfile, sep = "\t", skiprows = 8)
	mut_array = pd.read_csv(mutfile, sep = "\t", skiprows = 8)
	
	wt_energy = wt_array["Interaction Energy"].tolist()[0]
	mut_energy = mut_array["Interaction Energy"].tolist()[0]
	ddg =  mut_energy - wt_energy
	ddg_list.append([mutation, wt_energy, mut_energy, ddg])
    
    os.chdir("../")
  
ddg_frame = pd.DataFrame(ddg_list)
ddg_frame.to_csv("./Binding_DDG_summary.csv", header = False, index = False)
