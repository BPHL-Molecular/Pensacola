# Pensacola
A Nextflow pipeline to analyze *Candida auris* long-sequencing data from PacBio. The QC, species identification and species abundance of a sample, contig assembly, SNP calling and annotation, drug resistance detection, *etc* are included in the pipeline.  

![Picture1](https://github.com/user-attachments/assets/d386f6c8-1ed7-4805-8a77-2e8ed6ac13dd)

## Prerequisites
Nextflow is needed. The detail of installation can be found in https://github.com/nextflow-io/nextflow. For HiPerGator users, its installation is not needed. 

Singularity/APPTAINER is needed. The detail of installation can be found in https://singularity-tutorial.github.io/01-installation/. For HiPerGator users, its installation is not needed.

SLURM is needed. For HiPerGator users, its installation is not needed.

Python3 is needed. The package "pandas" should be installed by ``` pip3 install pandas ``` if not included in your python3.

LongQC is needed. Please install it to your local computer from its github repository (https://github.com/yfukasawa/LongQC). For HiPerGator users, its installation is not needed.

PacBio SMRTLINK stand-alone tools are needed. About how to install them, please see the file "How_to_install_smrtlink_tools.txt" in the pipeline.

The Kraken2/Bracken Refseq index--PlusPF is needed. Please download PlusPF index (over 77 GB) from the link (https://benlangmead.github.io/aws-indexes/k2) to the "PlusPF" folder in your local computer. And then extract the tar.gz archive. For HiPerGator users, its downloading is not needed. It has been downloaded and configed in the pipeline.

## Recommended conda environment installation
   ```bash
   conda create -n PENSACOLA -c conda-forge python=3.10 pandas
   ```
   ```bash
   conda activate PENSACOLA
   ```

## Reference
1. In this pipeline, the latest genome annotation of *Candida.auris* strain B8441 is used as the reference. They are available from http://www.candidagenome.org/download/sequence/C_auris_B8441/current/.
2. If you want to use another *Candida.auris* strain as the reference in the pipeline, please refer to the guide "How to build custom snpeff database using snpeff docker image in the pipeline.txt" in the pipeline.

## How to run

1. Rename your data files and make them looks like "bc2024bc2024.bam.pbi" and "bc2024bc2024.bam". You can use to the script "rename.sh" in the pipeline to rename your data files.
2. put the renamed data files (*.bam and *.bam.pbi) into the directory /pbbams.
3. open file "params.yaml", set the full paths of the parameters.   
   **input** : the full path to pbbams dir of the pipeline in your computer. It looks like "/\<the full path to the pipeline dir in your computer\>/pbbams".    
   **output** : the full path to output dir of the pipeline in your computer. It looks like "/\<the full path to the pipeline dir in your computer\>/output".            
   **reference** : the full path to reference dir of the pipeline in your computer. It looks like "/\<the full path to the pipeline dir in your computer\>/reference".    
   **snpeffconfig** : the full path to configs dir of the pipeline in your computer. It looks like "/\<the full path to the pipeline dir in your computer\>/configs".      
          
   **db** : the full path to kraken/bracken-database (PlusPF) in your computer. It looks like "/\<the full path to the parent dir of PlusPF foler in your computer\>/PlusPF".    
   **qc** : the full path to LongQC dir in your computer. It looks like "/\<the full path to the parent dir of LongQC foler in your computer\>/LongQC".     
           
   **Note: For HiperGator users, the parameters "db" and "qc" do not need to be changed. Just keep default settings.**     

4. get to the top directory of the pipeline, run 
```bash
sbatch ./pensacola.sh
```
#### Note: If you want to get email notification when the pipeline running ends, please input your email address in the line "#SBATCH --mail-user=<EMAIL>" in the batch file that you will run (namely, pensacola.sh).       

## Phylogeny and Molecular Evolution - Optional      
Pensacola use PhaME_m (https://github.com/BPHL-Molecular/PhaME_m) for phylogeny and molecular evolution of Candida samples. Three phylogenetic trees (FastTree, RaxML, IQ tree) can be generated.       
Please follow the steps below to perform phylogenetic analysis:       
1. Install required dependencies using mamba. Only applicable for the first time you use this feature.If this is not your first time using this feature, you don't need to reinstall them and please ignore this step.    
```bash
mamba install perl-bioperl
mamba install samtools
mamba install bcftools
mamba install mummer
mamba install bowtie2
mamba install fasttree
mamba install bbmap
mamba install raxml
mamba install perl-parallel-forkmanager
mamba install perl-statistics-distributions
mamba install paml
mamba install mafft
mamba install hyphy
```      
2. Go to /Phame directory    
3. Create the folder "/Phame/test/workdirs/mytest"
```bash
mkdir -p ./test/workdirs/mytest
```
4. Copy the contig files in fasta format of Candida samples to /Phame/test/workdirs/mytest/. The contig files were generated by Pensacola and outputted to the folder "assemble".
5. Optional- Change the default parameter settings. The default parameter settings can be changed in "./test/ctl_files/candida.ctl". For example, the default phylogenetic tree is RaxML. If you want IQ tree, you need change the parameter "tree = 2" to "tree = 3".
6. Run the file "phame.sh"      
```bash
sbatch ./phame.sh
```     
7. All phylogeny results can be found in the directory /Phame/test/workdirs/mytest/      
    
8. Note: 1. It makes no sense to perform bootstrap with less than 4 sequences. 2. Alignment must have at least 3 sequences.



 
