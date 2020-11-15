import random


items = [(random.randrange(2, 30), random.randrange(1, 20))for i in range(100)]
with open('output.txt', 'w') as out:
    for i in items:
        for j in i:
            out.write(str(j) + ' ')
        out.write('\n')
    out.close()
