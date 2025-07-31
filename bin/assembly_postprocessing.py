#!/usr/bin/env python3

import sys
import re
import argparse
import os


def assembly_postprocessing(assembly_input, sample_id, dropped_samples, assembly_header, read_depth_threshold):
    """Process assembly file and generate processed file with renamed and filtered contigs"""

    output_path = "{}_assembly_processed.fasta".format(sample_id)
    contig_cntr = 1

    with open(dropped_samples, 'a') as dropped_file:
        if os.path.getsize(assembly_input) == 0:
            dropped_file.write(sample_id + '\n')
            dropped_file.close()

    with open(output_path, "w") as assembly_processed, open(assembly_input, 'r') as assembly_file:
        write_contig = True
        for line in assembly_file:
            if not line.startswith(">"):
                if write_contig:
                    assembly_processed.write(line)
                continue

            match = re.search(r"_([\d\.]+)$", line.strip())
            if match:
                cov = round(float(match.group(1)), 2)
            else:
                cov = 0.00
            new_header = ">{}_{}{}_{:.2f}\n".format(sample_id, assembly_header, contig_cntr, cov)
            line = new_header
            contig_cntr += 1
            write_contig = cov >= read_depth_threshold
            if write_contig:
                assembly_processed.write(line)

    print("Processed file written to: {}".format(output_path))


def parse_args(argv=None):
    """Define and immediately parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Rename assembly contigs and drop contigs below threshold avg. read depth",
        epilog="Example: python assembly_rename_contigs.py input.fasta sample_id assembly_header read_depth_threshold"
    )
    parser.add_argument(
        "input_fasta",
        metavar="FILE_IN",
        type=str,
        help="Input fasta file"
    )
    parser.add_argument(
        "sample_id",
        type=str,
        help="Sample ID",
    )
    parser.add_argument(
        "dropped_samples",
        type=str,
        help="Dropped files log",
    )
    parser.add_argument(
        "assembly_header",
        type=str,
        help="Assembly header",
    )
    parser.add_argument(
        "read_depth_threshold",
        type=float,
        help="Min avg. read depth threshold",
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Coordinate argument parsing and program execution."""
    args = parse_args(argv)
    assembly_postprocessing(
        args.input_fasta,
        args.sample_id,
        args.dropped_samples,
        args.assembly_header,
        args.read_depth_threshold
    )


if __name__ == "__main__":
    sys.exit(main())
