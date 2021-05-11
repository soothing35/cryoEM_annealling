# Modify test.star file and generate a new file noted as test1.star 

f = open('4-3718.star','r+')  # Open the file you want to change
lines = f.readlines() # Read each lines

#print(lines) 

g = open('4-3718ready.star' , 'w') # Open
index = 0
for line in lines:
    if '@' in line:
        index += 1
        num = str(index).zfill(7) # Transfer to str
        particle_inform = line.split()
        particle_inform[0] = num + "@4-3718.mrcs"
        #particle_inform[1] = "3718"
        sep = ' ' 
        print(sep.join(particle_inform))
        g.write(sep.join(particle_inform) + '\n')


g.close()
f.close()

'''
        if index in range(1,100001):
                particle_inform.append(' 37') 

        if index in range(100001,200001):
                particle_inform.append(' 374') 

        if index in range(200001,300001):
                particle_inform.append(' 4')
'''