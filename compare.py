#!/usr/bin/python
import os
import sys
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--i1","-i1",help="First file to compare  (same type of knowledge,ontology)")
    parser.add_argument("--i2","-i2", help="Second file to compare (same type of knowledge,ontology))")
    parser.add_argument("--output","-o",help="output file to store the comparison")
    args = parser.parse_args()
    return args

'''
function : parse the 6 files into 2 big dictionary of NK or LK, key by the ontology
input    : 3 files
output   : NK or LK dictionary
'''

def check(infile):
    dic   = {}
    for line in infile.readlines():
        line = line.strip().split('\t')
        protein = line[0]
        GO = line[1]
        if protein in dic:
            dic[protein].append(GO)
        else:
            dic[protein] = [GO]
    return dic

def compare(dic1,dic2):
    outlist = []
    for protein in dic1:
        if protein not in dic2:
            outlist.append(protein)
    return outlist

if __name__ == "__main__":

    args = get_arguments()
    i1 = args.i1
    dic1 = check(open(i1,'r'))
    i2 = args.i2
    dic2 = check(open(i2,'r'))
    outfile  = args.output
    outfile = open(outfile,'w')
    outlist1 = compare(dic1,dic2)
    outlist2 = compare(dic2,dic1)
    outfile.write("Proteins that appears in {} but not in {}: \n".format(i1,i2))
    for protein in outlist1:
        outfile.write(protein +'\n')
    outfile.write("Proteins that appears in {} but not in {}: \n".format(i2,i1))
    for protein in outlist2:
        outfile.write(protein +'\n')