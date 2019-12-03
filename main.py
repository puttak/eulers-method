import csv

# ----- Constants ----- #
tau = 5 # residence time (min)
k = 0.12 # rate constant (min^-1)
h = 0.5 # step size (min)
t = 0 # initial time (min)
Ea = 0.001 # relative error tolerance

# ----- Initial concentrations ----- #
CA0 = 20 # this one stays constant
CA1 = 0
CB1 = 0
CA2 = 0
CB2 = 0

header = ["t (min)", "CA0", "CA1", "CB1", "CA2", "CB2", "error"]
data = [] # initialize matrix for csv writing

def dCA1(CA1):
    return ((1/tau)*(CA0 - CA1) - k*CA1)

def dCB1(CA1, CB1):
    return ((-1/tau)*CB1 + k*CA1)

def dCA2(CA1, CA2):
    return ((1/tau)*(CA1 - CA2) - k*CA2)

def dCB2(CB1, CA2, CB2):
    return ((1/tau)*(CB1 - CB2) + k*CA2)

def error(CB2_old, CB2_new):
    if CB2_new == 0:
        return (1337) # note: the error is actually undef
    else:
        return ((abs(CB2_new - CB2_old)/CB2_new)*100)

e = 1337
while e > Ea:
    row = [""]*7
    row[0] = t
    row[1] = CA0
    row[2] = CA1
    row[3] = CB1
    row[4] = CA2
    row[5] = CB2
    if e == 1337:
        row[6] = str("-")
    else:
        row[6] = e
    print(row)
    t = t + h
    data.append(row)
    CA1 = CA1 + dCA1(row[2])*h
    CB1 = CB1 + dCB1(row[2], row[3])*h
    CA2 = CA2 + dCA2(row[2], row[4])*h
    temp = CB2
    CB2 = CB2 + dCB2(row[3], row[4], row[5])*h
    e = error(temp, CB2)

row = [""]*7
row[0] = t
row[1] = CA0
row[2] = CA1
row[3] = CB1
row[4] = CA2
row[5] = CB2
row[6] = e
data.append(row)

print("At time t =", t, "(min) the relative error of CB2 is less than", Ea)
print("CA1 =", CA1)
print("CB1 =", CB1)
print("CA2 =", CA2)
print("CB2 =", CB2)

with open("HW9_1.csv", 'w') as File:
    writer = csv.writer(File, delimiter = ',', lineterminator = '\n') # note, comma delimiter for excel
    writer.writerow(header)
    writer.writerows(data)