#!/usr/bin/python
'''
Program: Unit testing
Author : Huy Nguyen
Start  : 05/31/2017
End    : /2017
'''
import unittest
import os
import sys
import argparse
from Bio.UniProt import GOA
from create_benchmark import read_gaf,analyze

t1_name,t1_dic,all_protein_t1 = read_gaf("/home/huyn/Ataur/unit_test/1")
t2_name,t2_dic,all_protein_t2 = read_gaf("/home/huyn/Ataur/unit_test/2")
NK_dic,LK_dic= analyze(t1_dic,t2_dic,all_protein_t1)

class TestBenchmark(unittest.TestCase):
    def test_not_include(self):
        for protein in ["A2P2R3","A2P2R4","A2P2R5","A2P2R6"]:
            for ontology in NK_dic:
                self.assertNotIn(protein,NK_dic[ontology],"This protein should not be in NK ")
        for protein in ["A2P2R3","A2P2R4","A2P2R5","A2P2R6"]:
            for ontology in LK_dic:
                self.assertNotIn(protein,LK_dic[ontology],"This protein should not be in LK ")
    def test_include_NK(self):
        self.assertIn("A5Z2X5",NK_dic["F"],"protein A5Z2X5 should gain knowledge in mfo in NK")
        self.assertIn("A5Z2X5",NK_dic["C"],"protein A5Z2X5 should gain knowledge in cco in NK")
        self.assertIn("A5Z2X5",NK_dic["P"],"protein A5Z2X5 should gain knowledge in bpo in NK")
        
        self.assertIn("I2HB52",NK_dic["F"],"protein I2HB52 should gain knowledge in mfo in NK")
        self.assertIn("I2HB52",NK_dic["C"],"protein I2HB52 should gain knowledge in cco in NK")
        self.assertNotIn("I2HB52",NK_dic["P"],"protein I2HB52 should not gain knowledge in bpo in NK")
        
        self.assertNotIn("I2HB70",NK_dic["F"],"protein I2HB70 should not gain knowledge in mfo in NK")
        self.assertNotIn("I2HB70",NK_dic["C"],"protein I2HB70 should not gain knowledge in cco in NK")
        self.assertIn("I2HB70",NK_dic["P"],"protein I2HB70 should gain knowledge in bpo")
    
    def test_include_LK(self):
        self.assertIn("O14464",LK_dic["F"],"protein O14464 should gain knowledge in mfo in LK")
        self.assertIn("O14464",LK_dic["C"],"protein O14464 should gain knowledge in cco in LK")
        self.assertNotIn("O14464",LK_dic["P"],"protein O14464 should not gain knowledge in bpo in LK")
        
        self.assertNotIn("O13563",LK_dic["F"],"protein O13563 should not gain knowledge in mfo in LK")
        self.assertNotIn("O13563",LK_dic["C"],"protein O13563 should not gain knowledge in cco in LK")
        self.assertIn("O13563",LK_dic["P"],"protein O13563 should gain knowledge in bpo in LK")
               
if __name__ == '__main__':
    unittest.main()
        