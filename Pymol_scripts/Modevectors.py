'''
Modified from http://www.pymolwiki.org/index.php/Modevectors

We addad some codes to fit our individual demands:
Besides alpha carbon (Ca), we also added phosphorus (P) to the list of calculation (line 27)
We also added a system to color the cylinders in according to their length (line 140-184)
'''
from __future__ import print_function
from pymol.cgo import *    # get constants
from math import *
from pymol import cmd


def modevectors(first_obj_frame, last_obj_frame, first_state=1, last_state=1, outname="modevectors", head=1.0, tail=0.3, head_length=1.5, cutoff=4.0, skip=0, cut=0.5, stat="show", factor=1.0, notail=0):
    

    framefirst = cmd.get_model(first_obj_frame, first_state)
    framelast = cmd.get_model(last_obj_frame, last_state)
    objectname = outname
    factor = float(factor)
    arrow_head_radius = float(head)
    arrow_tail_radius = float(tail)
    arrow_head_length = float(head_length)
    cutoff = float(cutoff)
    skip = int(skip)
    cut = float(cut)
    atomtype = ("CA","P")
    objectname = objectname.strip('"[]()')

    version = cmd.get_version()[1]
    arrow = []
    arrowhead = []
    arrowtail = []
    x1 = []
    y1 = []
    z1 = []
    x2 = []
    y2 = []
    z2 = []
    exit_flag = False
    f = open('translation_distance.txt', 'w')

    skipcount = 0
    skipcounter = 0
    keepcounter = 0
    atom_lookup = {}

    for atom in framefirst.atom:
        
        if atom.name in atomtype:
            if skipcount == skip:
                x1.append(atom.coord[0])
                y1.append(atom.coord[1])
                z1.append(atom.coord[2])
                #print("Atom is" + atom.name)


                current_atom = "CHAIN " + atom.chain + " RESID "\
                    + atom.resi + " RESTYPE "\
                    + atom.resn +\
                    " ATMNUM " + str(atom.index)

                atom_lookup['current_atom'] = 1

                skipcount = 0
                keepcounter += 1
            else:

                skipcount += 1
                skipcounter += 1

    skipcount = 0
    for atom in framelast.atom:
        if atom.name in atomtype:
            if skipcount == skip:
                x2.append(atom.coord[0])
                y2.append(atom.coord[1])
                z2.append(atom.coord[2])

             

                current_atom = "CHAIN " + atom.chain + " RESID "\
                    + atom.resi + " RESTYPE "\
                    + atom.resn +\
                    " ATMNUM " + str(atom.index)

                if 'current_atom' not in atom_lookup:
                    print("\nError: " + current_atom + " from \""\
                          + last_obj_frame +\
                          " \"is not found in \"" + first_obj_frame + "\".")
                    print("\nPlease check your input and/or selections and try again.")
                    exit_flag = True
                    break

                skipcount = 0
            else:
                skipcount += 1

    if exit_flag == 1:
     
        return

    cutoff_counter = 0  # Track number of atoms failing to meet the cutoff



    if len(x2) != len(x1):
        print("\nError: \"" + first_obj_frame +\
              "\" and \"" + last_obj_frame +\
              "\" contain different number of residue/atoms.")
        print("\nPlease check your input and/or selections and try again.")
        return
    else:

        save_view = cmd.get_view(output=1, quiet=1)
        cmd.delete(objectname)
        cmd.hide(representation="everything", selection=first_obj_frame)
        cmd.hide(representation="everything", selection=last_obj_frame)

    arrowtail = []
    for mv in range(len(x1)):
        vectorx = x2[mv] - x1[mv]
        vectory = y2[mv] - y1[mv]
        vectorz = z2[mv] - z1[mv]
        length = sqrt(vectorx ** 2 + vectory ** 2 + vectorz ** 2)
        if length < cutoff:
            cutoff_counter += 1
            continue
        t = 1.0 - (cut / length)
        x2[mv] = x1[mv] + factor * t * vectorx  # factor will multiply with vector length
        y2[mv] = y1[mv] + factor * t * vectory
        z2[mv] = z1[mv] + factor * t * vectorz
        vectorx = x2[mv] - x1[mv]
        vectory = y2[mv] - y1[mv]
        vectorz = z2[mv] - z1[mv]
        length = sqrt(vectorx ** 2 + vectory ** 2 + vectorz ** 2)
        d = arrow_head_length  # Distance from arrow tip to arrow base
        t = 1.0 - (d / length)

        #Color the cylinder according to the distance#

        print(length)
        print_length = str(length)+"\n"
        f.write(print_length)
        color_index = (length/2)
        if 1 < color_index <= 2:
            color_index1 = color_index - 1
            tr = hr = 0
            tg = hg = (int(color_index1 * 155))/255
            tb = hb = 1
        elif 2 < color_index <= 3:
            color_index2 = color_index -2
            decrease_index = color_index2 * 255
            tr = hr = 0
            tg = hg = 1
            tb = hb = (int(255 - decrease_index))/255
        elif 3 < color_index <= 4:
            color_index3 = color_index - 3
            tr = hr = (int(color_index3 * 255))/255
            tg = hg =1
            tb = hb = 0
        elif 4 < color_index <= 5:
            color_index4 = color_index - 4
            decrease_index=color_index4 * 100
            tr = hr = 1
            tg = hg = (int(255- decrease_index))/255
            tb = hb = 0
        elif 5 < color_index <= 6:
            color_index5 = color_index - 5
            decrease_index = color_index5 * 150
            tr = hr = 1
            tg = hg = (int(255 - decrease_index))/255
            tb = hb = 0
        elif color_index >6 :
            tr=hr=1
            tg=hg=0
            tb=hb=0
        elif color_index <1:
            tr=hr=0
            tg=hg=0
            tb=hb=1
            

        ######################################
        if notail:
            t = 0
        tail = [
            # Tail of cylinder
            CYLINDER, x1[mv], y1[mv], z1[mv]\
            , x1[mv] + (t + 0.01) * vectorx, y1[mv] + (t + 0.01) * vectory, \
            z1[mv] + (t + 0.01) * vectorz\
            , arrow_tail_radius, tr, tg, tb, tr, tg, tb  # Radius and RGB for each cylinder tail
        ]
        if notail == 0:
            arrow.extend(tail)


        x = x1[mv] + t * vectorx
        y = y1[mv] + t * vectory
        z = z1[mv] + t * vectorz
        dx = x2[mv] - x
        dy = y2[mv] - y
        dz = z2[mv] - z
        seg = d / 100
        intfactor = int(factor)
        if version < 1.1:  # Version >= 1.1 has cone primitive
            for i in range(100, 0, -1):  # i=100 is tip of cone
                print(i)
                t1 = seg * i
                t2 = seg * (i + 1)
                radius = arrow_head_radius * (1.0 - i / (100.0))  # Radius of each disc that forms cone
                head = [
                    CYLINDER, x + t2 * dx, y + t2 * dy, z + t2 * dz\
                    , x + t1 * dx, y + t1 * dy, z + t1 * dz\
                    , radius, hr, hg, hb, hr, hg, hb  # Radius and RGB for slice of arrow head
                ]
                arrow.extend(head)
        else:
            head = [
                CONE, x, y, z, x + d * dx, y + d * dy, z + d * dz, arrow_head_radius,
                0.0, hr, hg, hb, hr, hg, hb, 1.0, 1.0]
            arrow.extend(head)
    #print(arrow)



    if stat == "show":
        natoms = skipcounter + keepcounter
        print("\nTotal number of atoms = " + str(natoms))
        print("Atoms skipped = " + str(skipcounter))
        if keepcounter - cutoff_counter > 0:
            print("Atoms counted = " + str(keepcounter - cutoff_counter)
                  + " (see PyMOL object \"" + objectname + "\")")
        else:
            print("Atoms counted = " + str(keepcounter - cutoff_counter)
                  + " (Empty CGO object not loaded)")
        print("Atoms cutoff  = " + str(cutoff_counter))  # Note that cutoff occurs AFTER skipping!
    if keepcounter - cutoff_counter > 0:
        cmd.delete(objectname)
        cmd.load_cgo(arrow, objectname)
        # Ray tracing an empty object will cause a segmentation fault.  No arrows = Do not display in PyMOL!!!
    cmd.show(representation="ribbon", selection=first_obj_frame)
    if (first_obj_frame != last_obj_frame):
        cmd.show(representation="ribbon", selection=last_obj_frame)
        cmd.hide(representation="ribbon", selection=last_obj_frame)
    cmd.bg_color(color="white")
    cmd.set_view(save_view)
    return

cmd.extend("modevectors", modevectors)
