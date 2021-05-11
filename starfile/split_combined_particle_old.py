
sep =' '
for class_number in range(1,51):
    star_file_name = ""
    starfile_name4 = "4degree_" + class_number + "_of_50.star"
    starfile_name37 = "37degree_" + class_number + "_of_50.star"
    starfile_name374 = "374degree_" + class_number + "_of_50.star"

    star_file = open(star_file_name, 'r')
    star_lines = star_file.readlines()

    for star_line in star_lines:
        star_entries = star_line.split()

        if star_entries[4] == 4:
            f = open(starfile_name4, 'a')
            star_entries.append("\n")
            f.write(sep.join(star_line))
            f.close()

        if star_entries[4] == 37:
            f = open(starfile_name37, 'a')
            star_entries.append("\n")
            f.write(sep.join(star_line))
            f.close()

        if star_entries[4] == 374:
            f = open(starfile_name374, 'a')
            star_entries.append("\n")
            f.write(sep.join(star_line))
            f.close()

    star_file.close()
    count4 = len(open(starfile_name4, 'rU').readlines())
    count37 = len(open(starfile_name37, 'rU').readlines())
    count374 = len(open(starfile_name374, 'rU').readlines())
    with open('count4','a+') as a:
        a.write('count4'+ "\n")
    with open('count37', 'a+') as b:
        b.write('count37' + "\n")
    with open('count374', 'a+') as b:
        b.write('count374' + "\n")

