# CAFA benchmark
## Sypnosis
A quick program to create CAFA benchmark, need more exhaustive testing
## Installation
User can either use github interface Download or type the following command in command line:
```bash
git clone https://github.com/nguyenngochuy91/CAFA_benchmark
```
User has to install python, and biopython (would recommend use anaconda package). 
## Usage:
Within this directory when you clone it, the YEAST directory (downloaded from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old/YEAST/ ) will provide input for creating the benchmark, users are encourage to test it on more database
To create CAFA benchmark, choose the appropriate gfa files for t1, t2 time and a valid direction for ouput
```bash
./create_benchmark.py -t1 YEAST/gene_association.goa_ref_yeast.23 -t2 YEAST/gene_association.goa_ref_yeast.52 -o output
```
The six files benchmark will be created in output directory with names indicate which knowledge (NK or LK), and ontology (bpo,cco,mfo). 

## Testing:
We have also include the 2 file 1 and 2 in unit folder for testing purpose. Users can modify the files and the unit_test.py program to do unit testing. The unit_test already include some cases cover for the NK and LK knowledge. In order to run it, users can use this command line:

```bash
./unit_test.py
```
