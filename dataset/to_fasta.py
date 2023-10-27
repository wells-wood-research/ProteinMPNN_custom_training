from itertools import chain
import pandas as pd
import hashlib

import csv
def optimized_create_fasta_from_csv(csv_file, pdb_file, fasta_output_file):
    # Load list.csv and store the first and last columns in a dictionary
    chainid_to_sequence = {}
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)  # Skip the header row
        for row in reader:
            chainid = row[0]
            sequence = row[-1]
            chainid_to_sequence[chainid] = sequence

    # Load unique_pdb_codes.txt
    with open(pdb_file, 'r') as pdbs:
        unique_pdb_codes = set(line.strip() for line in pdbs)

    # Pre-filter sequences based on unique pdb codes
    pdb_to_sequences = {}
    for chainid, sequence in chainid_to_sequence.items():
        pdb_code = chainid.split('_')[0]
        if pdb_code in unique_pdb_codes:
            if pdb_code not in pdb_to_sequences:
                pdb_to_sequences[pdb_code] = []
            pdb_to_sequences[pdb_code].append((chainid, sequence))

    # Write sequences to FASTA file
    with open(fasta_output_file, 'w') as fasta:
        for pdb, sequences in pdb_to_sequences.items():
            for chainid, sequence in sequences:
                fasta.write(f">{chainid}\n{sequence}\n")
def create_fasta_from_csv(csv_file, pdb_file, fasta_output_file):
    # Load list.csv and store the first and last columns in a dictionary
    chainid_to_sequence = {}
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)  # Skip the header row
        for row in reader:
            chainid = row[0]
            sequence = row[-1]
            chainid_to_sequence[chainid] = sequence

    # Load unique_pdb_codes.txt
    with open(pdb_file, 'r') as pdbs:
        unique_pdb_codes = [line.strip() for line in pdbs]

    # For each unique PDB code, find the corresponding sequence and write to FASTA file
    with open(fasta_output_file, 'w') as fasta:
        for pdb in unique_pdb_codes:
            for chainid, sequence in chainid_to_sequence.items():
                if chainid.startswith(pdb):
                    fasta.write(f">{chainid}\n{sequence}\n")

# Example usage:
optimized_create_fasta_from_csv("original/list.csv", "unique_pdb_codes.txt", "sequences.fasta")