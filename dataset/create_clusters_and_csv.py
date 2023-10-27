import os
import pandas as pd
from sklearn.model_selection import train_test_split
import glob
import hashlib
# Optimized code for processing MMSeqs data

def parse_input_db(input_db_path):
    """Parse the input.db file to extract sequence identifiers and sequences."""
    sequences_data = []
    is_identifier = True
    with open(input_db_path, 'r') as file:
        for line in file:
            line = line.strip()
            if is_identifier:
                current_id = line
                is_identifier = False
            else:
                sequences_data.append((current_id, line))
                is_identifier = True
    return sequences_data

def parse_alignment_files(alignment_db_dir):
    """Parse all alignment.db.* files and extract alignment or cluster information."""
    alignment_data = []
    alignment_files = sorted(glob.glob(os.path.join(alignment_db_dir, "alignment.db.*")))
    for alignment_file in alignment_files:
        with open(alignment_file, 'r') as file:
            for line in file:
                parts = line.strip().split("\t")
                if len(parts) >= 2:
                    alignment_data.append((parts[0], parts[1]))
    return alignment_data

def generate_md5(seq):
    """Generate MD5 hash for a sequence."""
    return hashlib.md5(seq.encode()).hexdigest()

def create_dataframe(sequences_data, alignment_data):
    """Create a DataFrame for list.csv."""
    df = pd.DataFrame({
        'CHAINID': [item[0] for item in sequences_data],
        'DEPOSITION': 'NA',
        'RESOLUTION': 'NA',
        'HASH': [generate_md5(item[1]) for item in sequences_data],
        'CLUSTER': [item[1] for item in alignment_data][:len(sequences_data)],
        'SEQUENCE': [item[1] for item in sequences_data]
    })
    return df

def split_clusters(df_list):
    """Split clusters for validation and testing."""
    unique_clusters = df_list['CLUSTER'].unique()
    return train_test_split(unique_clusters, test_size=0.2, random_state=42)

def save_files(df_list, valid_clusters, test_clusters, output_dir):
    """Save the generated data to the output directory."""
    df_list.to_csv(os.path.join(output_dir, "list.csv"), index=False)
    with open(os.path.join(output_dir, "valid_clusters.txt"), 'w') as file:
        for cluster in valid_clusters:
            file.write(f"{cluster}\n")
    with open(os.path.join(output_dir, "test_clusters.txt"), 'w') as file:
        for cluster in test_clusters:
            file.write(f"{cluster}\n")

# New function to parse chain IDs
def parse_chain_ids(input_db_h_path):
    """Parse the input.db_h file to extract chain IDs."""
    chain_ids = []
    with open(input_db_h_path, 'r', errors='replace') as file:
        for line in file:
            chain_ids.append(line.strip())
    return chain_ids

# Updated main function
def process_mmseqs_data_updated(input_db_path, input_db_h_path, alignment_db_dir, output_dir):
    sequences_data = parse_input_db(input_db_path)
    alignment_data = parse_alignment_files(alignment_db_dir)
    chain_ids = parse_chain_ids(input_db_h_path)
    cleaned_chain_ids = [cid.replace('\x00', '') for cid in chain_ids]
    
    # Create DataFrame with the cleaned chain IDs
    df_list = pd.DataFrame({
        'CHAINID': cleaned_chain_ids[:len(sequences_data)],
        'DEPOSITION': 'NA',
        'RESOLUTION': 'NA',
        'HASH': [generate_md5(item[1]) for item in sequences_data],
        'CLUSTER': [item[1] for item in alignment_data][:len(sequences_data)],
        'SEQUENCE': [item[1] for item in sequences_data]
    })
    
    valid_clusters, test_clusters = split_clusters(df_list)
    save_files(df_list, valid_clusters, test_clusters, output_dir)
    print("Processing completed!")

# Call the function
process_mmseqs_data_updated("input.db", "input.db_h", ".", ".")

