f = open('3718_3.star', 'r+')
lines = f.readlines()
g = open('3718_4.star', 'w')
sep=' '

for line in lines:
    if '@' in line:
        column = line.split()
        item6 = column.pop(5)
        item7 = column.pop(5)
        item17 = column.pop(14)

        column.insert(13,item6)
        column.insert(14,item7)
        column.insert(13,item17)
        column.append("\n")
        g.write(sep.join(column))

g.close()
f.close()
