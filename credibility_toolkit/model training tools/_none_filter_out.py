

infile = "__conspiracy_features_training.csv"
outfile = "__conspiracy_features_training_filt.csv"
with open(infile) as f:
    for line in f:
        if "None" in line:
            continue
        with open(outfile, "a") as out:
            out.write(line)
            
            
        
        
    

            
