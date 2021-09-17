import gurobipy
import sys
from math import floor

# Inequalties of DDT
conv = (
-1, -1, 0, -1, 0, 0, 1, 0, 2,
0, 0, 1, 0, -1, -1, 0, -1, 2,
-1, 3, -2, -1, -2, -2, -1, 3, 6,
0, -1, 0, -1, 1, 2, 1, 2, 0,
-2, 2, -2, 1, 3, 3, 1, 2, 0,
3, 2, 3, 2, -2, -1, 1, -1, 0,
0, -1, 1, -1, 0, -1, 1, -1, 3,
-1, -1, -2, 3, -2, 3, -1, -2, 6,
0, -2, -1, -2, 0, 1, 2, 1, 3,
2, -1, 1, 1, 0, -2, -2, 1, 3,
-1, -2, -2, 1, 3, -2, 2, 1, 4,
2, 1, 1, -1, 0, 1, -2, -2, 3,
3, 1, -1, 1, -1, 1, -2, 1, 1,
-2, 2, 1, -2, 1, -2, -1, 1, 5,
2, 3, 1, 3, 1, -2, -1, -2, 1,
0, 1, 2, 1, -1, 2, -1, 2, 0,
-2, 1, -2, 2, 3, 2, 1, 3, 0,
-1, 1, -2, -2, 3, 1, 2, -2, 4,
-2, -2, 1, 2, 1, 1, -1, -2, 5,
1, -1, -1, -1, 0, -1, -1, -1, 5,
0, -1, -1, -1, 1, -1, -1, -1, 5,
)


# Inequalties of DDT with probability varaibles
convpbl = (
0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 1,
0, -1, 0, -1, 0, -1, 0, -1, 4, 3, 0,
0, 0, 0, 0, 0, 1, -1, 1, 1, 0, 0,
-1, 3, -2, -1, -2, -2, -1, 3, 6, 6, 0,
0, 1, -2, 1, 0, 1, -2, 1, 4, 1, 0,
3, 1, 2, -2, 0, 1, -3, -2, 5, 4, 0,
-2, 4, 3, -2, -1, -3, -2, -1, 6, 8, 0,
1, 2, 0, 2, 0, 1, 0, 1, -1, -2, 0,
3, 1, -1, 1, 0, -2, -1, -2, 3, 5, 0,
3, -2, 2, 1, 0, -2, -3, 1, 5, 4, 0,
-2, -2, 3, 4, -1, -1, -2, -3, 6, 8, 0,
3, 2, 6, 2, -2, -1, 1, -1, -3, 0, 0,
-2, 2, -1, 2, 5, -1, -5, -1, 5, 8, 0,
0, 1, -1, 1, 1, -1, 1, -1, 3, 1, 0,
-5, -2, 1, -3, 2, 5, 6, -3, 2, 9, 0,
-5, -3, 1, -2, 2, -3, 6, 5, 2, 9, 0,
2, -1, -2, -4, 1, 5, 2, 0, 2, 5, 0,
2, -5, -2, -1, 1, -1, 2, 6, 3, 7, 0,
0, -1, 0, -1, 1, 2, 3, 2, -2, 0, 0,
-1, -1, -2, 3, -2, 3, -1, -2, 6, 6, 0,
)

P_U = (
      3, 7, 6, 4, 1, 0, 2, 5, 11, 15, 14, 12, 9, 8, 10, 13
    )
P_V = (
      10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    )
ROUND = int(sys.argv[1])#7
act = [3, 5, 6, 7, 7, 8, 9, 12, 15, 20, 30, 40, 73, 40, 47, 52, 57, 61, 66]
#act =  [6, 6, 6, 6, 2, 2, 2, 2, 2, 2, 6, 6, 6, 6, 6, 6, 6, 6]
act_total = int(sys.argv[2])
FindList = []
if (sys.argv[3] == "fix"):
    fix = True
else:
    fix = False
fix_diff = [0x0000a000000a000f0000000fa7000550]
fix_pos = [0]
#fix_diff = [0x00000000001100000000000000000000,0x0090000000c000000000000000000000]
#fix_pos = [1,2]

fix_diff_bin = [bin(diff)[2:].zfill(128) for diff in fix_diff];
fix_bit = [];
for diff_1 in fix_diff_bin:
    fix_bit.append([len(diff_1)-1-i for i in range(0,len(diff_1)) if diff_1[i]=="1" ])
    
def PrintFirst(FindList,BanList):
    MILPFirst = open("WARP_First_"+str(ROUND)+".lp",'w+')
    MILPFirst.write("Minimize\n")
    buf = ''
    for i in range(0,ROUND):
        for j in range(0,32,2):
            buf = buf + "a" + str(i) + "_" + str(j)
            if i != ROUND-1 or j != 30:
                buf = buf + " + "
    MILPFirst.write(buf)
    MILPFirst.write('\n')
    MILPFirst.write("Subject to\n")
    ##################
    if (fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            fix_s_box_next = [floor((i)/4) for i in fix_bit[b]]
            #fix_s_box_prev = [floor(P_U.index(int((int(i/2) + int(i%2))/4))*2) for i in fix_bit[b]]
            for j in range(0,32,2):
                    #if (fix_pos!=0):
                    #    if(j in fix_s_box_prev):
                    #        buf = buf + "a" + str(fix_pos[b]-1) + "_" + str(j) + " = 1\n"
                    #    else:
                    #        buf = buf + "a" + str(fix_pos[b]-1) + "_" + str(j) + " = 0\n"
                    if (fix_pos!=ROUND):
                        if(j in fix_s_box_next):
                            buf = buf + "a" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                        else:
                            buf = buf + "a" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"
            MILPFirst.write(buf)
    #################
    ##################
    if (fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            for j in range(0,128):
                if(j in fix_bit[b]):
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                else:
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"
            MILPFirst.write(buf)
    #################
    #######Fix active sbox for 1st round#############
    
    # buf = ''
    # for i in range(0,1):
    #     for j in range(0,32,2):
    #         buf = buf + "a" + str(i) + "_" + str(j)
    #         if j != 30:
    #             buf = buf + " + "
    #         else:
    #             buf = buf + " = "
    
    # buf = buf + str(act[0]) + "\n"
    # MILPFirst.write(buf)
	###############
    ################Fix In and Out###############
    # buf = ''
    # for j in range(0,128):
    #     buf = buf + "x" + str(0) + "_" + str(j) + " - x"+ str(ROUND) + "_" + str(j) +" = 0 \n"
    # MILPFirst.write(buf)
    ################Fix In and Out###############
    buf = ''
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,32,2):
            buf = ''
            for k in range(0,4):
                buf = buf +  "x" + str(i) + "_" + str(4*j+k)
                if k != 3:
                    buf = buf + " + "
            buf = buf + " - a" + str(i) + "_" + str(j) + " >= 0\n"
            for k in range(0,4):
                buf = buf + "x" + str(i) + "_" + str(4*j+k) + " - a" + str(i) + "_" + str(j) + " <= 0\n"
            for k in range(0,4):
                buf = buf + "x" + str(i+1) + "_" + str(4*j+k+4) + " - x" + str(i)+ "_" +str(4*j+k) + " = 0\n"
            for k in range(0,4):
                buf = buf + "v" + str(i) + "_" + str(P_V[int(j/2)]*4 + k)  + " - x" + str(i)+ "_" + str(4*int(j+1)+k) + " = 0\n"
            for k in range(0,4):
                buf = buf + "u" + str(i) + "_" + str(4*int(j/2) + k) + " + v" + str(i) + "_" + str(4*int(j/2) + k) + " - x" + str(i+1) + "_" + str(4*j + k)  + " >= 0"+ "\n"
                buf = buf + "u" + str(i) + "_" + str(4*int(j/2) + k) + " - v" + str(i) + "_" + str(4*int(j/2) + k) + " + x" + str(i+1) + "_" + str(4*j + k)  + " >= 0"+ "\n"
                buf = buf + "- 1 u" + str(i) + "_" + str(4*int(j/2) + k) + " + v" + str(i) + "_" + str(4*int(j/2) + k) + " + x" + str(i+1) + "_" + str(4*j + k)  + " >= 0"+ "\n"
                buf = buf + "u" + str(i) + "_" + str(4*int(j/2) + k) + " + v" + str(i) + "_" + str(4*int(j/2) + k) + " + x" + str(i+1) + "_" + str(4*j + k)  + " <= 2"+ "\n"


            for k in range(0,21):
                for l in range(0,9):
                    if conv[9*k+l] > 0:
                        if l <= 3:
                            buf = buf + " + " + str(conv[9*k+l]) + " x" + str(i) + "_" + str(4*j+3-l)
                        if 4 <= l and l <= 7:
                            #buf = buf + " + " + str(conv[9*k+l]) + " x" + str(i+1) + "_" + str(P128[4*j+7-l])
                            buf = buf + " + " + str(conv[9*k+l]) + " u" + str(i) + "_" + str(P_U[int(j/2)]*4 + 7-l)
                        if l == 8:
                            buf = buf + " >= -" + str(conv[9*k+l]) + "\n"
                    if conv[9*k+l] < 0:
                        if l <= 3:
                            buf = buf + " - " + str(-conv[9*k+l]) + " x" + str(i) + "_" + str(4*j+3-l)
                        if 4 <= l and l <= 7:
                            #buf = buf + " - " + str(-conv[9*k+l]) + " x" + str(i+1) + "_" + str(P128[4*j+7-l])
                            buf = buf + " - " + str(-conv[9*k+l]) + " u" + str(i) + "_" + str(P_U[int(j/2)]*4 + 7-l)
                        if l == 8:
                            buf = buf + " >= " + str(-conv[9*k+l]) + "\n"
                    if conv[9*k+l] == 0:
                        if l == 8:
                            buf = buf + " >= " + str(conv[9*k+l]) + "\n"
            MILPFirst.write(buf)
                 
    buf = ''
    if len(FindList) == 0:
        for i in range(0,128):
            buf = buf + "x0_" + str(i)
            if i != 127:
                buf = buf + " + "
            if i == 127:
                buf = buf + " >= 1\n"
        for i in BanList:
            for j in range(0,len(i)):
                buf = buf + "a" + str(i[j][0]) + "_" + str(i[j][1])
                if j != len(i)-1:
                    buf = buf + " + "
                else:
                    buf = buf + " <= " + str(len(i)-1) + '\n'
    else:    
        fl = []
        for i in range(0,128):
            fl.append(i)
            if fl in FindList:
                #print(fl)
                #print("iii")
                buf = buf + "x0_" + str(i) + " = 1\n"
            else:
                buf = buf + "x0_" + str(i) + " = 0\n"
            fl.pop()
    MILPFirst.write(buf)

    buf = ''
    for i in range(0,ROUND):
        for j in range(0,32,2):
            buf = buf + "a" + str(i) + "_" + str(j)
            if i != ROUND-1 or j != 30:
                buf = buf + " + "
            else:
                buf = buf + " >= "
    
    buf = buf + str(act_total) + "\n"
    MILPFirst.write(buf)

    MILPFirst.write("Binary\n")
    buf = ''
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,32,2):
            buf = buf + "a" + str(i) + "_" + str(j) + "\n"
        MILPFirst.write(buf)
    for i in range(0,ROUND+1): ######################ROUND+1 for final charactertistics
        buf = ''
        for j in range(0,128):
            buf = buf + "x" + str(i) + "_" + str(j) + "\n"
        MILPFirst.write(buf)
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,64):
            buf = buf + "u" + str(i) + "_" + str(j) + "\n"
        MILPFirst.write(buf)
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,64):
            buf = buf + "v" + str(i) + "_" + str(j) + "\n"
        MILPFirst.write(buf)
	
    MILPFirst.close()


def PrintSecond(SolveList,ftl):
    MILPSecond = open("WARP_Second_"+str(ROUND)+".lp","w+")
    MILPSecond.write("Minimize\n")
    buf = ''
    
    for i in range(0,len(SolveList)):
        buf = buf + " 2 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0 + 3 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1"
        if i != len(SolveList)-1:
            buf = buf + " + "
        else:
            buf = buf + "\n"
    MILPSecond.write(buf)
    MILPSecond.write("Subject to\n")
     ##################
    if (fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            for j in range(0,128):
                if(j in fix_bit[b]):
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                else:
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"
            MILPSecond.write(buf)
    #################
    ################Fix In and Out###############
    # buf = ''
    # for j in range(0,128):
    #     buf = buf + "x" + str(0) + "_" + str(j) + " - x"+ str(ROUND) + "_" + str(j) +" = 0 \n"
    # MILPSecond.write(buf)
    ################Fix In and Out###############
    buf = ''
    for i in range(0,len(SolveList)):
        buf = ''
        
            
        for k in range(0,4):
            buf = buf + "4 x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
            if k != 3:
                buf = buf + " + "
        for k in range(0,4):
            buf = buf + " - y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
        buf = buf + " >= 0\n"

        for k in range(0,4):
            buf = buf + "4 y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
            if k != 3:
                buf = buf + " + "
        for k in range(0,4):
            buf = buf + " - x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+k)
        buf = buf + " >= 0\n"
        MILPSecond.write(buf)
    
        buf = ''
        for k in range(0,20):
            for l in range(0,11):
                if convpbl[11*k+l] > 0:
                    if l <= 3:
                        buf = buf + " + " + str(convpbl[11*k+l]) + " x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+3-l)
                    if 4 <= l and l <= 7:
                        buf = buf + " + " + str(convpbl[11*k+l]) + " y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+7-l)
                    if 8 <=l and l <= 9:
                        buf = buf + " + " + str(convpbl[11*k+l]) + " z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l-8)
                    if l == 10:    
                        buf = buf + " >= -" + str(convpbl[11*k+l]) + "\n"
                if convpbl[11*k+l] < 0:
                    if l <= 3:
                        buf = buf + " - " + str(-convpbl[11*k+l]) + " x" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+3-l)
                    if 4 <= l and l <= 7:
                        buf = buf + " - " + str(-convpbl[11*k+l]) + " y" + str(SolveList[i][0]) + "_" + str(4*SolveList[i][1]+7-l)
                    if 8 <= l and l <= 9:
                        buf = buf + " - " + str(-convpbl[11*k+l]) + " z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l-8)
                    if l == 10:
                        buf = buf + " >= " + str(-convpbl[11*k+l]) + "\n"
                if convpbl[11*k+l] == 0:
                    if l == 10:
                        buf = buf + " >= " + str(convpbl[11*k+l]) + "\n"

        MILPSecond.write(buf)
    
    buf = ''
    sl = []
    for i in range(0,ROUND):
        buf = ''
        sl = []
        sl.append(i)
        for j in range(0,32,2):
            sl.append(j)

            if sl not in SolveList:
                for k in range(0,4):
                    buf = buf + "x" + str(i) + "_" + str(4*j+k) + " = 0\n"
                    buf = buf + "y" + str(i) + "_" + str(4*j+k) + " = 0\n"
            sl.pop()
            for k in range(0,4):
                buf = buf + "u" + str(i) + "_" + str(P_U[int(j/2)]*4 + k) + " - y" + str(i)+ "_" +str(int(j)*4 + k) + " = 0\n"
            for k in range(0,4):
                buf = buf + "x" + str(i+1) + "_" + str(4*j+k+4) + " - x" + str(i)+ "_" +str(4*j+k) + " = 0\n"
            for k in range(0,4):
                buf = buf + "v" + str(i) + "_" + str(P_V[int(j/2)]*4 + k)  + " - x" + str(i)+ "_" + str(4*int(j+1)+k) + " = 0\n"
            for k in range(0,4):
                buf = buf + "u" + str(i) + "_" + str(4*int(j/2) + k) + " + v" + str(i) + "_" + str(4*int(j/2) + k) + " - x" + str(i+1) + "_" + str(4*j + k)  + " >= 0"+ "\n"
                buf = buf + "u" + str(i) + "_" + str(4*int(j/2) + k) + " - v" + str(i) + "_" + str(4*int(j/2) + k) + " + x" + str(i+1) + "_" + str(4*j + k)  + " >= 0"+ "\n"
                buf = buf + "- 1 u" + str(i) + "_" + str(4*int(j/2) + k) + " + v" + str(i) + "_" + str(4*int(j/2) + k) + " + x" + str(i+1) + "_" + str(4*j + k)  + " >= 0"+ "\n"
                buf = buf + "u" + str(i) + "_" + str(4*int(j/2) + k) + " + v" + str(i) + "_" + str(4*int(j/2) + k) + " + x" + str(i+1) + "_" + str(4*j + k)  + " <= 2"+ "\n"

        MILPSecond.write(buf)

   
    buf = ''
    if len(ftl) == 0:
        for i in SolveList:
            if i[0] == 0:
                buf = buf + "x0_" + str(4*i[1]) + " + x0_" + str(4*i[1]+1) + " + x0_" + str(4*i[1]+2) + " + x0_" + str(4*i[1]+3)
                buf = buf + " >= 1\n"
        MILPSecond.write(buf)
    else:
        fl = []

        for i in range(0,128):
            fl.append(i)
            if fl in ftl:
                buf = buf + "x0_" + str(i) + " = 1\n"
            else:
                buf = buf + "x0_" + str(i) + " = 0\n"
            fl.pop()
        MILPSecond.write(buf)
    

    MILPSecond.write("Binary\n")
    buf = ''
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,128):
            buf = buf + "x" + str(i) + "_" + str(j) + "\n"
        for j in range(0,32,2):
            for k in range(0,4):
                buf = buf + "y" + str(i) + "_" + str(j*4+k) + "\n"
        for j in range(0,64):
            buf = buf + "u" + str(i) + "_" + str(j) + "\n"
        for j in range(0,64):
            buf = buf + "v" + str(i) + "_" + str(j) + "\n"
        MILPSecond.write(buf)
    buf = ''
    for j in range(0,128):
        buf = buf + "x" + str(ROUND) + "_" + str(j) + "\n"
    MILPSecond.write(buf)
    buf = ''
    for i in range(0,len(SolveList)):
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0\n"
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1\n"
        MILPSecond.write(buf)
        buf = ''
    MILPSecond.close()

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
def strtoint2(s):
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
    result.append(int(s2))
    return result

count = 0
count1 = 0
FindSBoxList = []
fsl = []
fslstring = []
resreg = 128
FindTailList = []
ftl = []
ftlstring = []
BanList = []
bl = []
blstring = []
filename = "WARP_Result_" + str(ROUND) + ".txt"
opResult = open(filename,'w+')
#############FIX Active S-Box##################
# #bl = [[0, 0], [0, 2], [1, 0], [1, 8], [2, 4], [2, 6], [3, 1], [3, 9], [4, 0], [4, 2], [5, 0], [5, 8], [6, 4], [6, 6], [7, 1], [7, 9], [8, 0], [8, 2], [9, 0], [9, 8], [10, 4], [10, 6],[11,0],[11,1],[11,2],[11,3],[11,4],[11,5],[11,6],[11,7],[11,8],[11,9],[11,10],[11,11],[11,12],[11,13],[11,14],[11,15]];
# bl = [[0,1],[0, 10],[1, 0], [1, 2], [2, 0], [2, 8], [3, 4], [3, 6], [4, 1], [4, 9], [5, 0], [5, 2], [6, 0], [6, 8], [7, 4], [7, 6], [8, 1], [8, 9], [9, 0], [9, 2], [10, 0], [10, 8], [11, 4], [11, 6], [12, 1], [12, 9]];
# #bl = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,15],[1, 0], [1, 2], [2, 0], [2, 8], [3, 4], [3, 6], [4, 1], [4, 9], [5, 0], [5, 2], [6, 0], [6, 8], [7, 4], [7, 6], [8, 1], [8, 9], [9, 0], [9, 2], [10, 0], [10, 8], [11, 4], [11, 6], [12, 1], [12, 9]];
# # bl = [[0,1],[0, 8]];
# BanList.append(bl)
# BanListlen = len(bl)
# print(bl)
# PrintInner(bl)
# while True:
#     i = gurobipy.read("Inner_"+str(ROUND)+".lp")
#     i.optimize()
#     buf = ''
#     buf = buf + str(bl) + " " + str(i.getObjective().getValue()) + "\n"
#     if i.getObjective().getValue() < resreg:
#         resreg = i.getObjective().getValue()
#         ot = open("mini_"+str(ROUND)+".txt","w+")
#         ot.write(str(resreg))
#         ot.close()
#     for v in i.getVars():
#         if v.x == 1:
#             buf = buf + v.VarName + " "
#     buf = buf + "\n"
#     opResult.write(buf)
#     opResult.flush()
# opResult.close()
#############FIX Active S-Box##################
while True:
    count = 0
    
    fsl = []
    fslstring = []
    ftl = []
    ftlstring = []
    bl = []
    opResult.write("*\n*\n*\n")
    while True:
        PrintFirst(ftl,BanList)
        count = count + 1
        
        if count == 15:
            break
        o = gurobipy.read("WARP_First_"+str(ROUND)+".lp")
        o.optimize()
        #o.write("128_Outer_"+str(ROUND)+".sol")
        #sys.exit()
        obj = o.getObjective()
        try:
            if obj.getValue() <= (act_total + 128):
                fsl = []
                fslstring = []
                for v in o.getVars():
                    if v.x == 1 and v.VarName[0] == 'a':
                        fslstring.append(v.VarName)
                for f in fslstring:
                    fsl.append(strtoint(f))
                if count == 1:
                    for f in fslstring:
                        bl.append(strtoint(f))
                    BanList.append(bl)
                    print("*\n*\n*\n*\n")
                    print(BanList)
                    print("*\n*\n*\n*\n")
                
                print(fsl)
                PrintSecond(fsl,ftl)
                ftl = []
                i = gurobipy.read("WARP_Second_"+str(ROUND)+".lp")
                i.optimize()
                if i.getObjective().getValue() > 135:
                    break
                buf = ''
                buf = buf + str(fsl) + " " + str(i.getObjective().getValue()) + "\n"
                ftlstring = []
                for v in i.getVars():
                    if v.x == 1:
                        buf = buf + v.VarName + " "
                    if v.x == 1 and v.VarName[0] == 'x' and v.VarName[1] == str(ROUND-2):
                        ftlstring.append(v.VarName)
                for f in ftlstring:
                    ftl.append(strtoint2(f))

                buf = buf + "\n"
                opResult.write(buf)
                opResult.flush()
    
            else:
                break
        except:
            break
            continue;
opResult.close()
