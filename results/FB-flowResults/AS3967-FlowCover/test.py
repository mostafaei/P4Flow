file1 = open('portSet.txt', 'r')
portLists = file1.readlines()
print(type(portLists))
for i in range(len(portLists)):
    print(portLists[i])
