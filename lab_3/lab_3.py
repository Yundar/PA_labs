p = 500
items = []
with open('E:\Study\PA\PA_labs\output.txt', 'r') as inp:
    for i in range(100):
        items.append(list(map(int, inp.readlines(1)[0].split())))
print(items)
