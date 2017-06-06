#!/usr/bin/python
'''
Program: creating CAFA benchmark
Author : Huy Nguyen
Start  : 05/31/2017
End    : 05/31/2017
'''
import os
import sys
import argparse
from Bio.UniProt import GOA

'''
argument parsers
'''
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--t1","-t1",help="t1 file")
    parser.add_argument("--t2","-t2", help="t2 file")
    parser.add_argument("--output","-o",help="output directory to store the 6 benchmark file")
    args = parser.parse_args()
    return args
'''
function : given a file handle, parse in using gaf format and return a dictionary
           that identify those protein with experimental evidence and the ontology
input    : file text
output   : dic (key: name of file (number), value is a big dictionary store info about the protein)
'''
def read_gaf(handle):
    name = handle.split(".")[-1]
    dic = {}
    all_protein_name = set()
    # evidence from experimental
    Evidence = {'Evidence': set(['EXP','IDA','IPI','IMP','IGI','IEP'])}
    with open(handle, 'r') as handle:
        for rec in GOA.gafiterator(handle):
            all_protein_name.add(rec['DB_Object_ID'])
            if GOA.record_has(rec, Evidence) and rec['DB'] == 'UniProtKB':
                if rec['DB_Object_ID'] not in dic:
                    dic[rec['DB_Object_ID']] = {rec['Aspect']:set([rec['GO_ID']])}  
                else:
                    if rec['Aspect'] not in dic[rec['DB_Object_ID']]:
                        dic[rec['DB_Object_ID']][rec['Aspect']]=set([rec['GO_ID']])  
                    else:
                        dic[rec['DB_Object_ID']][rec['Aspect']].add(rec['GO_ID'])
    return name,dic ,all_protein_name
'''
function : given t1 dic, t2 dic, we provide the dic for NK, and LK dic for each ontology
input    : 2 dics
output   : NK,LK dictionary
'''
def analyze(t1_dic,t2_dic,all_protein_t1):
    NK_dic = {'P':{},'C':{},'F':{}}
    LK_dic = {'P':{},'C':{},'F':{}}
    # dealing with NK and LK
    
    for protein in t2_dic:
        ## check the protein in t2_dic but not appear in t1
        if protein not in t1_dic and protein in all_protein_t1: ## this going to be in NK
            ### check which ontology got new annotated
            for ontology in t2_dic[protein]:
                NK_dic[ontology][protein] = t2_dic[protein][ontology]
        ## check the protein that in t2_dic and appear in t1
        elif protein  in t1_dic :
            ## check if in t1, this protein does not have all 3 ontology
            ### if yes, then not include since full knowledge
            ### else
            if len(t1_dic[protein]) < 3:
                #### check if t2_dic include in the ontology that t1 lack of
                for ontology in t2_dic[protein]:
                    if ontology not in t1_dic[protein]: # for those lack, include in LK
                        LK_dic[ontology][protein] = t2_dic[protein][ontology]
    return NK_dic,LK_dic 
    
'''
function : given NK,LK dic , write out 6 files 
input    : 2 dics
output   : NK,LK dictionary
'''
def write_file(dic,knowledge,name):
    for ontology in dic:
        if ontology =='F':
            final_name = name+knowledge+'_mfo'
        elif ontology =='P':
            final_name = name+knowledge+'_bpo'
        elif ontology =='C':
            final_name = name+knowledge+'_cco'
        print "Writing {} file".format(final_name)
        file_out = open(final_name,'w')
        for protein in sorted(dic[ontology]):
            for annotation in dic[ontology][protein]:
                file_out.write(protein +'\t'+annotation+'\n')
        file_out.close()
    return None
    

if __name__ == "__main__":

    args = get_arguments()
    t1 = args.t1
    t2 = args.t2
    outdir  = args.output
    t1_name,t1_dic,all_protein_t1 = read_gaf(t1)
#    print "t1 \n",t1_dic
    t2_name,t2_dic,all_protein_t2 = read_gaf(t2)
#    print "t2 \n",t2_dic    
    NK_dic,LK_dic= analyze(t1_dic,t2_dic,all_protein_t1)
    try:
        os.mkdir(outdir)
    except:
        print "The directory has already been created"
    num1 = t1.split('.')[-1]
    num2 = t2.split('.')[-1]
    name = outdir+'/'+'.'.join(t1.split('/')[-1].split('.')[:-1])+'.'+num2+'-'+num1+'_benchmark_'
    write_file(NK_dic,'NK',name)
    write_file(LK_dic,'LK',name)
