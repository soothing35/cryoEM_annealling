f = open('3718_33.star', 'r+')
lines = f.readlines()  # Read each lines

# print(lines)

g = open('3718_44.star', 'w')  # Open
index = 0

target_column = []
target_column_num = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
real_column_number = [j + 1 for j in target_column_num]

for line in lines:
    if '@' in line:
        index += 1
        column = line.split()  # split elements in lines in to elements
        # print(column[4,5,7,8,11,12,13,14,15,19,23,24])

        for i in target_column_num:
            target_column.append(column[i])

        target_column.append('\n')
        # print(sep.join(target_column))
        print("Line number: " + str(index))

sep = ' '
g.write(sep.join(target_column))
print("Real number is " + str(real_column_number))

g.close()
f.close()
