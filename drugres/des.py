#!/usr/bin/env python

import glob
import os

# Define the output directory and file path
output_dir = "./"
report_file_path = os.path.join(output_dir, "Drug_resistance_report.txt")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Write the initial content to the report file
with open(report_file_path, "w") as f:
    f.write("########## Detected drug resistance ##########" + "\n\n")

# Open the drug resistance list file
file1 = open('./drugres_snpeff_list.csv')
filelist = glob.glob("./variants/*_snpeff.ann.vcf")

content1 = file1.readlines()
druglistlen = len(content1)

filenum = 0
for afile in filelist:
    filenum += 1
    paths = afile.strip().split("/")
    with open(report_file_path, "a") as f:
        f.write(str(filenum) + ". " + paths[-1] + ": \n\n")
        f.write(content1[0])

    with open(afile) as file2:
        content2 = file2.readlines()
        for aline in content2:
            if not aline.startswith("#"):
                tabitems = aline.strip().split("\t")
                
                # Check that tabitems has at least 8 elements
                if len(tabitems) > 7:
                    subtabs = tabitems[7].strip().split(";")
                else:
                    subtabs = []  # Handle case where tabitems[7] doesn't exist
                
                # Process subtabs if they exist
                for cell in subtabs:
                    if "ANN=" in cell:
                        anns = cell.strip().split(",")
                        for oneann in anns:
                            for indx in range(1, druglistlen):
                                cols = content1[indx].strip().split(",")
                                
                                # Check that cols has at least 4 elements
                                if len(cols) > 3:
                                    muts = []
                                    if ";" in cols[3]:
                                        cells = cols[3].strip().split(";")
                                        for x in cells:
                                            muts.append(x)
                                    else:
                                        muts.append(cols[3])
                                    
                                    if cols[0] in oneann:
                                        for amut in muts:
                                            if amut in oneann:
                                                with open(report_file_path, "a") as f:
                                                    f.write(content1[indx] + "\n\n")
                                else:
                                    continue
