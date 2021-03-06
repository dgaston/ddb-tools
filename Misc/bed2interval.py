__author__ = 'dgaston'

import argparse
import argcomplete

import pybedtools


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="input file (BED)")
    parser.add_argument('-o', '--outfile', help="Output file (GATK interval list)")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    intervals = pybedtools.BedTool(args.infile)

    with open(args.outfile, 'w') as output:
        for interval in intervals:
            output.write("%s:%s-%s\n" % (interval.chrom, interval.start + 1, interval.end + 1))
