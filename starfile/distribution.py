import matplotlib.pyplot as plt
import matplotlib

rotation_angle = []

f = open('rotation_angle-Copy1.txt' , 'r')
lines = f.readlines()
#print(lines)
for line in lines:
    x = float(line.strip())  #float: transfering string to float     strip: remove '\n'
    rotation_angle.append(x)
print(rotation_angle)


plt.hist(rotation_angle, bins=360, density=True)
plt.xticks([-180,-90,0,90,180])
plt.show()
f.close()