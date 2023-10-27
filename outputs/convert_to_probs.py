import os
import csv
import re

def one_hot_encode_sequence(sequence, amino_acid_map):
    """One-hot encodes a protein sequence."""
    # Removing 'X' characters from the sequence
    encoded = [[0.0] * 20 for _ in range(len(sequence))]
    for i, amino_acid in enumerate(sequence):
        if amino_acid in amino_acid_map:
            index = list(amino_acid_map.keys()).index(amino_acid)
            encoded[i][index] = 1.0
    return encoded

def extract_designed_chains(description):
    """Extracts the designed_chains value from the fasta description."""
    match = re.search(r'designed_chains=\[\'(.*?)\'\]', description)
    if match:
        return match.group(1)
    return ""

def clean_sequence(sequence, valid_amino_acids):
    """Cleans the sequence by retaining only valid amino acids."""
    return ''.join([aa for aa in sequence if aa in valid_amino_acids])

def process_fasta_files_v2(folder_path, amino_acid_map, csv_output, txt_output):
    """Processes all fasta files in the given folder, extracting the second sequence."""
    proteins = []
    with open(csv_output, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for fasta_file in sorted(os.listdir(folder_path)):
            if fasta_file.endswith(".fa"):
                with open(os.path.join(folder_path, fasta_file), 'r') as file:
                    lines = file.readlines()
                    if len(lines) < 4:
                        print(f"Skipping {fasta_file} as it has fewer than 4 lines.")
                        continue
                    designed_chains = extract_designed_chains(lines[0])
                    protein_name = fasta_file.split('.')[0] + designed_chains
                    # Cleaning the sequence
                    sequence = clean_sequence(lines[3].strip(), amino_acid_map.keys())
                    encoded_sequence = one_hot_encode_sequence(sequence, amino_acid_map)
                    writer.writerows(encoded_sequence)
                    
                    proteins.append((protein_name, len(sequence)))
                    
    with open(txt_output, 'w') as txt_file:
        txt_file.write("ignore_uncommon False\ninclude_pdbs\n##########\n")
        for protein, length in proteins:
            txt_file.write(f"{protein} {length}\n")

# Define the amino acid map
standard_amino_acids = {
    "A": "ALA",
    "C": "CYS",
    "D": "ASP",
    "E": "GLU",
    "F": "PHE",
    "G": "GLY",
    "H": "HIS",
    "I": "ILE",
    "K": "LYS",
    "L": "LEU",
    "M": "MET",
    "N": "ASN",
    "P": "PRO",
    "Q": "GLN",
    "R": "ARG",
    "S": "SER",
    "T": "THR",
    "V": "VAL",
    "W": "TRP",
    "Y": "TYR",
}

# Specify paths
folder_path = "epoch_50/"
csv_output = f"ProteinMPNN_{folder_path}.csv"
txt_output = f"ProteinMPNN_{folder_path}.txt"

# Run the function
process_fasta_files_v2(folder_path, standard_amino_acids, csv_output, txt_output)

# Specify paths
folder_path = "epoch_150/"
csv_output = f"ProteinMPNN_{folder_path}.csv"
txt_output = f"ProteinMPNN_{folder_path}.txt"

# Run the function
process_fasta_files_v2(folder_path, standard_amino_acids, csv_output, txt_output)