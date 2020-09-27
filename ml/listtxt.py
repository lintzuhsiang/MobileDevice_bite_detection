import os, random
NUMBER_IN_LIST = 200
name_t = []
name_f = []

name_vt = []
name_vf = []

while len(name_t)< NUMBER_IN_LIST:
    file0 = random.choice(os.listdir('./true'))
    if file0 not in name_t:
        name_t.append('true/'+file0)


while len(name_f)< NUMBER_IN_LIST:
    file0 = random.choice(os.listdir('./false'))
    if file0 not in name_f:
        name_f.append('false/'+file0)


while len(name_vt)< NUMBER_IN_LIST:
    file0 = random.choice(os.listdir('./true'))
    if file0 in name_t:
        continue
    if file0 not in name_vt:
        name_vt.append('true/'+file0)

while len(name_vf)< NUMBER_IN_LIST:
    file0 = random.choice(os.listdir('./false'))
    if file0 in name_f:
        continue
    if file0 not in name_vf:
        name_vf.append('false/'+file0)

f = open('testlist.txt','w')
for i in name_t+name_f:
    f.write(i+'\n')

fv = open('validlist.txt','w')
for i in name_vt+name_vf:
    fv.write(i+'\n')

f.close()
fv.close()

