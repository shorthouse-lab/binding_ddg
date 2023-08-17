# binding_ddg calculations
## Code for calculating binding DDG using FoldX

This repository contains python scripts for running binding DDG calculations using FoldX (https://foldxsuite.crg.eu)

In order to run calculations, a FoldX license will need to be obtained, and the FoldX binary downloaded. The included scripts reference this binary, so make sure to replace the relevant line in each script to where you have placed yours.

Included are reproducible calculations and analysis to interpret and understand how missense mutations impact binding of proteins to each other, small molecules, and DNA.

#### Within the "scripts" directory there are 3 scripts that do a majority of the work:

* repair_multi.py - This script repairs and energy minimizes the structure.

* binding_ddg.py - This script calculates all "target" protein residues within a cutoff of the "ligand", then mutates each residue to every possible other residue, before calculating the energy change (DDG) of these mutations.

* summary_binding_ddg.py - This script summarises the DDG for each mutations and outputs a single file containing all the energies.

#### Also included in this repository are examples of use-cases and analysis:

* Barnase-barstar - Calculation of the effects of single and small groups of mutations on binding DDG.

* SPOP-BRD3 - Calculation of evidence of mutational selection of binding DDG in large-scale genomic data using an expected distribution.

* TP53-DNA - Calculation and comparison of binding DDG with clinical and other data.

* PARP1-niraparib - Calculation of the effects of mutations on drug binding and resistance.

Communication: d.shorthouse (at) ucl.ac.uk
