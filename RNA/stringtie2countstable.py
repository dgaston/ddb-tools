#!/usr/bin/env python

import sys
import argparse
import HTSeq
from collections import defaultdict
from ddb import configuration


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input config file for samples")
    parser.add_argument('-c', '--configuration', help="Configuration file for various settings")
    parser.add_argument('-o', '--output', help="Output file name for CSV file")
    args = parser.parse_args()

    sys.stdout.write("Parsing configuration data\n")
    config = configuration.configure_runtime(args.configuration)

    sys.stdout.write("Parsing sample data\n")
    samples = configuration.configure_samples(args.input, config)

    transcript_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for sample in samples:
        sys.stderr.write("Processing sample {}\n".format(sample))
        gtf_file = HTSeq.GFF_Reader(samples[sample]['gtf'], end_included=True)
        for feature in gtf_file:
            # sys.stderr.write("Processing entry: {}\n".format(feature))
            if feature.type is 'transcript':
                transcript_counts[feature.attr['transcript_id']][sample]['FPKM'] = feature.attr['FPKM']
                transcript_counts[feature.attr['transcript_id']][sample]['TPM'] = feature.attr['TPM']

    with open(args.output, 'w') as output:
        output.write("Transcript")
        for sample in samples:
            output.write("\t{sample} FPKM\t{sample} TPM".format(sample=sample))
        output.write("\n")
        for transcript in transcript_counts:
            output.write("{}".format(transcript))
            for sample in samples:
                output.write("\t{}\t{}".format(transcript_counts[transcript][sample]['FPKM'],
                                               transcript_counts[transcript][sample]['TPM']))
            output.write("\n")
