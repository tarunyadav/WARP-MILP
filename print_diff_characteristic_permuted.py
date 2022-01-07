import sys

permute_in = (11, 18, 9, 20,7, 30, 5, 22,3,16,1,28,31,24,29,26,27,2,25,4,23,14,21,6,19,0,17,12,15,8,13,10)
permute_out = (31,18,29,20,27,30,25,22,23,16,21,28,19,24,17,26,15,2,13,4,11,14,9,6,7,0,5,12,3,8,1,10)
WARP_permute = (0, 19, 2, 21, 8, 31, 12, 23, 14, 17,6, 29,26, 25, 20, 27, 16, 3, 18, 5, 24, 15, 28, 7, 30, 1, 22, 13, 10, 9, 4, 11)

filename = sys.argv[1]
blocksize= 128;
f1 = open(filename,"r");
data = f1.readlines()
data_copy = [a for a in data];
for a in data_copy:
    if ("*" in a):
        data.remove(a)
#print(data)
f1.close()
diff_sbox_line = data[2*int(sys.argv[2]) - 2]
diff_differential_line = data[2*int(sys.argv[2]) - 1]

diff_prob = diff_sbox_line.split("]]")[1].strip()
diff_differential_line_arr = diff_differential_line.split()

def print_binary_data(data,prob):
    for i in range(0,len(data),4):
        print(data[i:i+4],end='  ');
    print(":: Hex => ",end='');
    for i in range(0,len(data),16):
        print(hex(int(data[i:i+16],2))[2:].zfill(4),end='  ')
    print(" :: ",end='0x')
    for i in range(0,len(data),16):
        print(hex(int(data[i:i+16],2))[2:].zfill(4),end='')
    print(" :: Probability => 2^{-"+str(prob)+"} :: No. of Active S-Box => " +str(int(prob/2)) )
    print("");

def strtoint(s):
    reg = 0
    s1 = ''
    s2 = ''
    result = []
    for i in range(0,len(s)):
        if s[i] == '_':
            reg = 1
        if s[i] >= '0' and s[i]<= '9':
            if reg == 0:
                s1 = s1 + s[i]
            if reg == 1:
                s2 = s2 + s[i]
    result.append(int(s1))
    result.append(int(s2))
    return result
round_bit_arr  = []
round_bit_arr_y = []
prob_arr = []
for var in diff_differential_line_arr:
    if (var[0] == 'x'):
        round_bit_arr += [strtoint(var)]
    elif (var[0] == 'y'):
        round_bit_arr_y += [strtoint(var)]
    elif (var[0] == 'z'):
        new_var = var.split("_");
        prob_arr += [strtoint("_".join([new_var[0],new_var[2]]))]
no_of_rounds = max([_[0] for _ in round_bit_arr])


print("Differential Probability for " + str(no_of_rounds) + " rounds of WARP_"+str(blocksize)+" is 2^{-" + str(diff_prob) + "} :: Total No. of Active S-Box => " +str(int(float(diff_prob)/2)))
for r in range(0,no_of_rounds+1):
    print("The input difference of the round "+ str(r)+" is: ");
    diff_bits = list("0"*blocksize);
    active_bits = [a[1] for a in round_bit_arr if a[0]==r]
    for bit in active_bits:
        diff_bits[len(diff_bits)-1-bit] = "1";

    probability = 0;
    if (r>0):
        round_prob  = [a[1] for a in prob_arr if a[0]==r-1]
        for prob in round_prob:
            if (prob==0):
                probability += 2;
            elif (prob==1):
                probability += 3;
    final_bits_arr = []
    if (r==0):
       bits  = "".join(diff_bits)
       bits_arr = [bits[i:i+4] for i in range(0,len(bits),4)]
       for i in range(0,len(bits_arr)):
           final_bits_arr.append(bits_arr[len(bits_arr)-1-permute_in[i]])
       print_binary_data("".join(final_bits_arr),probability);
       
    elif(r==no_of_rounds):
        bits  = "".join(diff_bits)
        bits_arr = [bits[i:i+4] for i in range(0,len(bits),4)] 
        for i in range(0,len(bits_arr),2):
            temp_bits = bits_arr[i]
            bits_arr[i] = bits_arr[i+1]
            bits_arr[i+1] = temp_bits
        for i in range(0,len(bits_arr)):
            final_bits_arr.append(bits_arr[len(bits_arr)-1-permute_out[i]])
        WARP_permute_arr = []
        for i in range(0,len(final_bits_arr)):
            WARP_permute_arr.append(final_bits_arr[len(final_bits_arr)-1-WARP_permute[i]])
        
        print_binary_data("".join(WARP_permute_arr),probability);
       
    else:
    	print_binary_data("".join(diff_bits),probability);
