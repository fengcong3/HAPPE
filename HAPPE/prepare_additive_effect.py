#coding:utf-8
# 参数提供的gzvcfs 决定了additive effect的方向，
# 输出的结果 从ref --> alt
import argparse
import sys,os


chr_list = ["chr1A","chr1B","chr1D","chr2A","chr2B","chr2D","chr3A","chr3B","chr3D", \
    "chr4A","chr4B","chr4D","chr5A","chr5B","chr5D","chr6A","chr6B","chr6D","chr7A","chr7B","chr7D"]
bcftools = "/public/agis/chengshifeng_group/fengcong/WGRS/software/bcftools1.9/bin/bcftools"
if __name__ == "__main__":
    cmdparser = argparse.ArgumentParser(description="prepare additive effect" )
    cmdparser.add_argument("-i","--input", dest="input",type=str,required=True,
                            help="gemma ouput")
    cmdparser.add_argument("-r","--region", dest="region",type=str,required=False,
                            help="region format. eg. chr1A:1-100.")
    cmdparser.add_argument("-s","--snplist", dest="snplist",type=str,required=False,
                            help="snplist.")
    cmdparser.add_argument('gzvcfs', metavar='gzvcfs', type=str, nargs='+',
                    help='gzvcfs,must named chr*.*.vcf.gz.')

    args = cmdparser.parse_args()
    input_file = args.input
    vcf_list = args.gzvcfs
    region = args.region if args.region else None
    if region:
        region_chr = region.split(":")[0]
        region_start = int(region.split(":")[1].split("-")[0])
        region_end = int(region.split(":")[1].split("-")[1])

    snplist = args.snplist if args.snplist else None
    snp_list = []
    if snplist:
        insnpf = open(snplist,"r")
        for line in insnpf:
            snp_list.append(line.strip())

    file_d = {}
    for vcf in vcf_list:
        file_d[ os.path.basename(vcf).split(".")[0] ] = vcf
        if os.path.exists(vcf+".csi"):
            pass
        else:
            if not os.system("bcftools index %s"%(vcf)):
                pass
            else:
                sys.stderr.write("bcftools index faild:%s\n"%(vcf))
                exit(-1)
    
    inf = open(input_file,"r")
    header = inf.readline().strip().split()

    chromo_index = header.index("chr")
    ps_index = header.index("ps")
    rs_index = header.index("rs")
    beta_index = header.index("beta")
    allele1_index = header.index("allele1")
    allele0_index = header.index("allele0")
    pvalue_index = header.index("p_wald")

    header1 = ["SNPid","p-value","additive_effect"]
    sys.stdout.write("\t".join(header1)+"\n")
    line = inf.readline()
    while line:
        ls = line.strip().split()
        if not snplist or ls[1] in snp_list:
            pass
        else:
            line = inf.readline()
            continue
        
        if not region or (region_chr == ls[chromo_index] and region_start <= int(ls[ps_index]) <= region_end ):
            pass
        else:
            line = inf.readline()
            continue

        tmpls = [ ls[rs_index] , ls[pvalue_index] ]
        rec = os.popen('%s view -r %s:%s-%s %s | tail -n 2'%(bcftools ,ls[chromo_index],ls[ps_index],ls[ps_index],file_d[ls[chromo_index]]))
        head = rec.readline()
        if not head.startswith("#CHROM"):
            tmpls.append("Unknown")
            sys.stdout.write("\t".join(tmpls)+"\n")
            line = inf.readline()
            continue

        rec = rec.readline()
        rec = rec.strip('\n').split()
        ref = rec[3]
        alt = rec[4]

        if ref == ls[allele1_index] and alt == ls[allele0_index]:
            beta1 = "-"+ls[beta_index] if not ls[beta_index].startswith("-") else ls[beta_index][1:]
        else:
            beta1 = ls[beta_index]
        
        tmpls.append(beta1)


        sys.stdout.write("\t".join(tmpls) + "\n")

        line = inf.readline()
    
    inf.close()