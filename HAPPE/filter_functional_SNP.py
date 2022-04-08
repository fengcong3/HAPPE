# filter functional SNPs
# usage: python3 filter_functional_SNP.py <input_file> | bgzip -c > <output_file>

import sys
import gzip
# from typing_extensions import Annotated
import SNPANN_upgrade_3

functional_or_not_d = {
    "3_prime_UTR_variant":0,
    "start_gain":1,
    "5_prime_UTR_variant":0,
    "start_gain":1,
    "3_prime_UTR_variant":0,
    "5_prime_UTR_variant":0,
    "downstream_gene_variant":0,
    "intergenic_region":0,
    "intron_variant":0,
    "splice_acceptor_variant":1,
    "splice_donor_variant":1,
    "splice_region_variant":0,
    "splice_acceptor_variant&splice_donor_variant":1,
    "splice_acceptor_variant":1,
    "splice_donor_variant":1,
    "stop_retained_variant":0,
    "start_lost":1,
    "stop_lost":1,
    "splice_region_variant":0,
    "missense_variant":1,
    "missense_variant":1,
    "start_lost":1,
    "stop_gained":1,
    "stop_gained":1,
    "stop_lost":1,
    "stop_retained_variant":0,
    "synonymous_variant":0,
    "upstream_gene_variant":0
}

if __name__ == "__main__":
    input_file = sys.argv[1]
    inf = gzip.open(input_file, 'rt') if input_file.endswith('.gz') else open(input_file, 'r')
    outf = sys.stdout
    for line in inf:
        if line.startswith('#'):
            outf.write(line)
        else:
            ls = line.strip().split()
            featureid,annotation,c_xx,p_xx = SNPANN_upgrade_3.SNP_ANN_of_Gene_Structure(ls[7])
            if annotation  not in functional_or_not_d:
                sys.stderr.write(line)
                sys.stderr.write("function annotaion error\n")
                exit(-1)
            if functional_or_not_d[annotation]:
                outf.write(line)
            

    inf.close()
    outf.close()
