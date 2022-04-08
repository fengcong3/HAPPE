#coding:utf-8
# fengcong@caas.cn
# created by fengcong on 2021-8-30 14:50:23
# convert vcf file to heatmap format

import sys
import argparse
import logging
import gzip
import os

# out put format
# name ref alt  sample1 sample2 sample3 ...
# chr1A_131 A G 0 9 -9 ...


logging.basicConfig(level = logging.DEBUG,format = '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',stream = sys.stderr)
logger = logging.getLogger("vcf2heatmatrix")

if __name__ == "__main__":
    cmdparser = argparse.ArgumentParser(description="convert vcf file to heatmap format./fengcong@caas.cn" )
    #general options
    cmdparser.add_argument("-v","--vcf", dest="vcf",type=str, required=True,
                            help="vcf file, can be gziped.")
    cmdparser.add_argument("-o","--out", dest="out",type=str, required=False,
                            help="output file, deafult = stdout.")
    
    args = cmdparser.parse_args()

    inf = gzip.open(args.vcf,"rt") if args.vcf.endswith(".gz") else open(args.vcf,"r")
    ouf = args.out if args.out else sys.stdout

    header_list = []
    for line in inf:
        if line.startswith("##"):
            continue
        if line.startswith("#"):
            header_list = line.strip().split()
            tmpls = ["name","ref","alt"] + header_list[9:]
            ouf.write("\t".join(tmpls)+"\n")
            del tmpls
            continue
        
        snp_list = line.strip().split()
        out_list = [snp_list[2], snp_list[3] , snp_list[4] ] 

        
        # output heat matrix
        for gt in snp_list[9:]:
            i = gt.split(":")[0]
            if i == "0/1" or i=="0|1" or i == "1|0": #het
                out_list.append("0")
            elif i == "0/0" or i == "0|0" :
                out_list.append("-9")
            elif i == "1/1" or i == "1|1" :
                out_list.append("9")
            else:
                out_list.append("NA")

        ouf.write("\t".join(out_list)+"\n")

    
    inf.close()
    ouf.close()

