# MMSeqs Commands from Justas and Ivan

#1. Convert .fa into mmseqs database:

mmseqs createdb sequences.fa input.db

#Prefilter the database:

mmseqs prefilter input.db input.db prefilter.db -s 7.5

#Align @ 30% sequence identity cutoff:

mmseqs align input.db input.db prefilter.db alignment.db --min-seq-id 0.3 --max-seqs 10000

#Convert results into tabular format:

mmseqs convertalis input.db input.db alignment.db alignment.db.tab