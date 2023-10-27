import pandas as pd

# 1. Read the file unique_pdb_codes.txt to obtain a list of PDB codes.
with open("unique_pdb_codes.txt", 'r') as f:
    pdb_codes = [line.strip() for line in f.readlines()]

# 2. Read the data from list.csv and filter rows where the PDB code is found in CHAINID.
data = pd.read_csv("original/list.csv")
filtered_data = data[data['CHAINID'].apply(lambda x: x.split('_')[0] in pdb_codes)]

# 3. Randomly sample 20% of the filtered data
sample_data = filtered_data.sample(frac=0.2)

# 4. Save the hashes of the sampled rows to valid_clusters.txt
sample_data['HASH'].to_csv("valid_clusters.txt", index=False, header=False)
