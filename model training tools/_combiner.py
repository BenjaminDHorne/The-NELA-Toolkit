
### assume three files 1.txt, 2.txt. 3.txt, all comma separated
### with userid as the first column.

def get_vals(fname):
    vals = {}
    f = open(fname)
    m = f.readline().strip().split(",")
    header = ",".join( m[1:] )
    for line in f:
        m = line.strip().split(",")
        vals[ m[0] ] = ",".join(m[1:])
    return vals, header


if __name__ == "__main__":
    feat1, header1 = get_vals("_conspiracy_groundtruth.csv")
    feat2, header2 = get_vals("all_features_training_conspiracy.csv")
    empty1 = ",".join( ["None"]*2 )  ## change 5 to number of features in file1
    empty2 = ",".join( ["None"]*230 )  ## change 5 to number of features in file2
    allids = set(feat1.keys() + feat2.keys())# + feat4.keys() + feat5.keys())

    fout = open("__conspiracy_features_training.csv", "w")
    fout.write( "pid,%s,%s\n" %(header1, header2))

    for userid in allids:
        
        if userid in feat1:
            line1 = feat1[userid]
        else:
            line1 = empty1

        if userid in feat2:
            line2 = feat2[userid]
        else:
            line2 = empty2

        fout.write("%s,%s,%s\n" %(str(userid),line1,line2))
    fout.close()

            
