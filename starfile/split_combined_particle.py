
sep =""
for class_number in range(1, 51):
	star_file_name = "norm_psi_Class50_" + str(class_number) + ".star"
	starfile_name4 = "4_" + str(class_number) + "_of_50.star"
	starfile_name37 = "37_" + str(class_number) + "_of_50.star"
	starfile_name374 = "374_" + str(class_number) + "_of_50.star"
	starfile_name3718 = "3718" + str(class_number) + "_of_50.star"
	star_head1 = "\ndata_images\n\n"
	star_head2 = "loop_\n"
	star_head3 = "_rlnImageName #1\n"
	star_head4 = "_rlnAngleRot #2\n"
	star_head5 = "_rlnAngleTilt #3\n"
	star_head6 = "_rlnAnglePsi #4\n"
	star_head7 = "_rlnMicrographName #5\n"
	with open(starfile_name4,'w')as aaa:
		aaa.write(star_head1)
		aaa.write(star_head2)
		aaa.write(star_head3)
		aaa.write(star_head4)
		aaa.write(star_head5)
		aaa.write(star_head6)
		aaa.write(star_head7)
	with open(starfile_name37,'w') as bbb:
		bbb.write(star_head1)
		bbb.write(star_head2)
		bbb.write(star_head3)
		bbb.write(star_head4)
		bbb.write(star_head5)
		bbb.write(star_head6)
		bbb.write(star_head7)
	with open(starfile_name374, 'w') as ccc:
		ccc.write(star_head1)
		ccc.write(star_head2)
		ccc.write(star_head3)
		ccc.write(star_head4)
		ccc.write(star_head5)
		ccc.write(star_head6)
		ccc.write(star_head7)
	with open(starfile_name3718, 'w') as ddd:
		ddd.write(star_head1)
		ddd.write(star_head2)
		ddd.write(star_head3)
		ddd.write(star_head4)
		ddd.write(star_head5)
		ddd.write(star_head6)
		ddd.write(star_head7)

for class_number in range(1,51):
	star_file_name = "norm_psi_Class50_" + str(class_number) + ".star"
	starfile_name4 = "4_" + str(class_number) + "_of_50.star"
	starfile_name37 = "37_" + str(class_number) + "_of_50.star"
	starfile_name374 = "374_"+ str(class_number) + "_of_50.star"
	starfile_name3718 = "3718" + str(class_number) + "_of_50.star"

	star_file = open(star_file_name, 'r')
	star_lines = star_file.readlines()
	
	
	for star_line in star_lines:
		if '@' in star_line:
			star_entries = star_line.split()

			if int(star_entries[4]) == 4:
				f = open(starfile_name4, 'a+')
				star_entries.append("\n")
				f.write(sep.join(star_line))
				f.close()
				print(sep.join(star_line))
			if int(star_entries[4]) == 37:
				f = open(starfile_name37, 'a+')
				star_entries.append("\n")
				f.write(sep.join(star_line))
				f.close()

			if int(star_entries[4]) == 374:
				f = open(starfile_name374, 'a+')
				star_entries.append("\n")
				f.write(sep.join(star_line))
				f.close()
			if int(star_entries[4]) == 3718:
				f = open(starfile_name3718, 'a+')
				star_entries.append("\n")
				f.write(sep.join(star_line))
				f.close()
	star_file.close()
	count4 = len(open(starfile_name4, 'rU').readlines())
	count37 = len(open(starfile_name37, 'rU').readlines())
	count374 = len(open(starfile_name374, 'rU').readlines())
	count3718 = len(open(starfile_name3718, 'rU').readlines())
	with open('count4.txt','a+') as a:
		a.write(str(count4) + "\n")
	with open('count37.txt', 'a+') as b:
		b.write(str(count37) + "\n")
	with open('count374.txt', 'a+') as c:
		c.write(str(count374) + "\n")
	with open('count3718.txt', 'a+') as d:
		d.write(str(count3718) + "\n")
