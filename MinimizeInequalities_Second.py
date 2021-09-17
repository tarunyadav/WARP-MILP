from __future__ import print_function
import numpy as np

def print_DDT(table):
    for row in range(len(table)):
        for col in range(len(table[row])):
            print(table[row][col],end='');
            if col == len(table[row])-1:
                print("\n");
def print_Diff(table):
    for row in range(len(table)):
        for col in range(len(table[row])):
            print(table[row][col],end='');
            if col == len(table[row])-1:
                print("");
def print_Diff_sage(table):
    for row in range(len(table)):
        print("[",end='');
        for col in range(len(table[row])):
            if col == len(table[row])-1:
                print(table[row][col],end=' ');
                print("],",end='');
            else:
                print(table[row][col],end=' , ');
   
  
s_box = ((0xc,0xa, 0xd,0x3, 0xe,0xb, 0xf, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6),);
           

DDT_SIZE = (len(s_box),len(s_box[0]))
DDT = np.zeros( (DDT_SIZE[1],DDT_SIZE[1]) )
DDT = DDT.astype(int)
sbox_val = []

for p2 in range(DDT_SIZE[1]):
    row = p2 >> 4
    col = p2 & 15
    sbox_val.append(s_box[row][col]);

for p1 in range(DDT_SIZE[1]):
	for p2 in range(DDT_SIZE[1]):
		XOR_IN = np.bitwise_xor(p1,p2);
		XOR_OUT = np.bitwise_xor(sbox_val[p1],sbox_val[p2]);
		DDT[XOR_IN][XOR_OUT] += 1

diff_arr = []
impossible_diff_arr=[]
for row in range(len(DDT)):
        row_bin = bin(row)[2:].zfill(4);
        row_arr = [int(i) for i in row_bin];
        for col in range(len(DDT[row])):
            col_bin = bin(col)[2:].zfill(4);
            col_arr = [int(i) for i in col_bin];
            if(DDT[row][col]!=0):
                #DDT_bin = bin(DDT[row][col])[2:].zfill(3);
                if (DDT[row][col] == 16):
                    DDT_bin = '00';
                elif (DDT[row][col] == 4):
                    DDT_bin = '01';
                elif (DDT[row][col] == 2):
                    DDT_bin = '10';
                int_DDT_bin = int(DDT_bin,2);
                DDT_arr = [int(i) for i in DDT_bin];
                diff_arr += [row_arr+col_arr+DDT_arr[::-1]];
                for k in range(0,4):
                    if (k!=int_DDT_bin):
                        im_bin = bin(k)[2:].zfill(2);
                        im_arr = [int(i) for i in im_bin];
                        impossible_diff_arr += [row_arr+col_arr+im_arr[::-1]];
            else:
                for k in range(0,4):
                        im_bin = bin(k)[2:].zfill(2);
                        im_arr = [int(i) for i in im_bin];
                        impossible_diff_arr += [row_arr+col_arr+im_arr[::-1]];
poly_test = Polyhedron( vertices = diff_arr)
ineq_list = poly_test.inequalities_list();
#######Optional: if user want to print all the inequalities###########################
#print(ineq_list);
ineq_fail_index = [];
ineq_fail_count = [0]*len(ineq_list);
lp_string=[]
lp_string += ["Minimize"];
ineq_str = "";
for i in range(0,len(ineq_list)):
    ineq_str += "z"+str(i)+" + ";
lp_string += [ineq_str[0:-3]];
lp_string += ["\n"];
lp_string += ["Subject To"];
for i in range(0,len(impossible_diff_arr)):
    imp_diff_arr = np.array([1] + impossible_diff_arr[i]);
    ineq_str_i = "";
    for j in range(0,len(ineq_list)):
        ineq_list_arr = np.array(ineq_list[j]);
        if(sum(imp_diff_arr*ineq_list_arr) < 0):
            ineq_fail_index += [(i,j)];
            ineq_str_i += "z"+str(j)+" + ";
    ineq_str_i = ineq_str_i[0:-3] + " >= 1"
    lp_string += [ineq_str_i];
lp_string += ["\n"];
lp_string += ["Binary"];
for i in range(0,len(ineq_list)):
    lp_string += ["z"+str(i)];
print(len(lp_string));
f1 = open("MinimizeInequalities_Second.lp","w");
for a in lp_string:
    f1.write(a+"\n");
f1.close();

#################Following code to be run once inequalities are minimized using MILP#####################
# ineq_list_rotated = [];
# for inq in ineq_list:
#     ineq_list_rotated += [inq[1:]+[inq[0]]]
# ineq_redunction = [0, 8, 136, 317, 357, 367, 532, 556, 584, 753, 803, 828, 929, 979, 1025, 1071, 1125, 1186, 1194, 1222]
# print(len(ineq_redunction))
# for i in ineq_redunction:
#     print(ineq_list_rotated[i])

