test = {}
test["castricum"] = {}
test["castricum"]["zaandam"] = 15
test["castricum"]["beverwijk"] = 8

for i in range(len(test["castricum"])):
    print(list(test["castricum"].items())[i][1])
