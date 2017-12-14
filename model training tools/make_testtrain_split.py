import random

testsize = 0.2
testfn = "./_newsVSconsp_train.csv"
trainfn = "./_newsVSconsp_test.csv"
allfn = "./_newsVSconspiracy_features_selected.csv"
with open(testfn, "a") as test:
    with open(trainfn, "a") as train:
        with open(allfn) as allpoints:
            header = allpoints.readline()
            test.write(header)
            train.write(header)
            for point in allpoints:
                if random.random() > 0.2:
                    test.write(point)
                else:
                    train.write(point)
