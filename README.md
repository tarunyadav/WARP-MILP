# WARP-MILP
MILP Based Differential Characteristics Search for Block Cipher WARP (https://link.springer.com/chapter/10.1007/978-3-030-81652-0_21) \

## Source Code
### There are 11 python files in this source code.
* _MinimizeInequality_First.py_
* _MinimizeInequality_Second.py_
* _MinimizeInequality_First.lp_
* _MinimizeInequality_Second.lp_
* _WARP_LinIneq_MILP.ipynb_
* _MinimizeInequality_First.sol_
* _MinimizeInequality_Second.sol_
* _Linear_Inequalities.txt_
* _MILP_Solve.py_
* _print_diff_characteristic.py_
* _README.md_

## Generation of Linear Inequalities
* ```MinimizeInequality_First.py``` generates linear inequalities (to reduce number of active S-boxes) using Sage (https://cocalc.com/ can be used to run Sage). It also generate MILP problem (```MinimizeInequality_First.lp```) to minimize the number of linear inequalities. This problem can be solved using ```GUROBI``` (gurobipy in https://colab.research.google.com/ - ```WARP_LinIneq_MILP.ipynb```). The solution is written in the ```MinimizeInequality_First.sol```. In this file, the inequalities after minimization are assigned the value 1. This solution is replaced on line 97 of ```MinimizeInequality_First.py```. Uncommenting last part of ```MinimizeInequality_First.py``` produces list of 21 linear inequalities which will be used in ```MILP_Solve.py```.
* ```MinimizeInequality_Second.py``` generates linear inequalities (to optimize probability of differential characteristics) using Sage (https://cocalc.com/ can be used to run Sage). It also generate MILP problem (```MinimizeInequality_Second.lp```) to minimize the number of linear inequalities. This problem can be solved using ```GUROBI``` (gurobipy in https://colab.research.google.com/ - ```WARP_LinIneq_MILP.ipynb```). The solution is written in the ```MinimizeInequality_Second.sol```. In this file, the inequalities after minimization are assigned the value 1. This solution is replaced on line 113 of ```MinimizeInequality_Second.py```. Uncommenting last part of ```MinimizeInequality_Second.py``` produces list of 20 linear inequalities which will be used in ```MILP_Solve.py```.\
**_(While minimzing linear inequalities using MILP, the number of inequalities will reamin same(21 and 20) but the inequalties may change.)_**

## MILP model to minimize number of active S-boxes and optimize probability of differential characteristics

* _MILP_Solve.py_ is used to model the MILP problem and solve it using ```GUROBI```. Linear inequalties generated in previous section have to be updated in this file. This file contains two modules First and Second. First modules minimizes number of active S-boxes while second module search for differential characteristics with high probability. Both these modules are interfaced together and user need not to run these separately. 
* _MILP_Solve.py_ takes three arguments. First argument defines number of rounds, second argument define the cutoff bound of active S-box and third argument is used to fix bits in the input. The second argument is made changable(instead of fix upper/lower bound) because it is obsevered that GUROBI gives quick solution for for some values which are not directly related to the upper/lower bound of active S-box. 
* High probablitiy differential characteristic for 18-round WARP is searched using following command:\
```MILP_Solve.py 18 22 fix_no```
* The output (_WARP_Result_18.txt_) is in the following format:
```
[[0, 6], [0, 14], [0, 22], [0, 28], [1, 14], [1, 26], [2, 2], [2, 26], [3, 2], [3, 16], [5, 4], [5, 22], [6, 12], [6, 24], [7, 4], [7, 10], [7, 18], [7, 24], [8, 18], [8, 30], [9, 6], [9, 12], [9, 24], [9, 26], [10, 4], [10, 6], [10, 8], [10, 16], [11, 0], [11, 2], [11, 8], [11, 12], [11, 14], [11, 22], [11, 26], [12, 2], [12, 6], [12, 10], [12, 14], [12, 16], [12, 24], [12, 26], [12, 28], [13, 2], [13, 8], [13, 16], [13, 18], [13, 28], [14, 4], [14, 12], [14, 16], [14, 20], [14, 26], [15, 6], [15, 12], [15, 22], [16, 0], [16, 14], [17, 0], [17, 6], [17, 26]] 122.0
z0_6_0 z0_14_0 z0_22_0 z0_28_0 z1_14_0 z1_26_0 z2_2_0 z2_26_0 z3_2_0 z3_16_0 z5_4_0 z5_22_0 z6_12_0 z6_24_0 z7_4_0 z7_10_0 z7_18_0 z7_24_0 z8_18_0 z8_30_0 z9_6_0 z9_12_0 z9_24_0 z9_26_0 z10_4_0 z10_6_0 z10_8_0 z10_16_0 z11_0_0 z11_2_0 z11_8_0 z11_12_0 z11_14_0 z11_22_0 z11_26_0 z12_2_0 z12_6_0 z12_10_0 z12_14_0 z12_16_0 z12_24_0 z12_26_0 z12_28_0 z13_2_0 z13_8_0 z13_16_0 z13_18_0 z13_28_0 z14_4_0 z14_12_0 z14_16_0 z14_20_0 z14_26_0 z15_6_0 z15_12_0 z15_22_0 z16_0_0 z16_14_0 z17_0_0 z17_6_0 z17_26_0 x0_24 x0_25 x0_26 x0_27 y0_24 y0_25 y0_26 y0_27 x0_57 x0_59 y0_56 y0_57 y0_58 y0_59 x0_89 x0_91 y0_88 y0_90 x0_113 x0_115 y0_112 y0_114 x1_56 x1_57 x1_58 x1_59 y1_57 y1_59 x1_104 x1_106 y1_105 y1_107 x2_9 x2_11 y2_8 y2_10 x2_104 x2_105 x2_106 x2_107 y2_105 y2_107 x3_8 x3_9 x3_10 x3_11 y3_8 y3_9 y3_10 y3_11 x3_65 x3_67 y3_65 y3_67 x5_17 x5_19 y5_17 y5_19 x5_88 x5_89 x5_90 x5_91 y5_88 y5_89 y5_90 y5_91 x6_49 x6_51 y6_49 y6_51 x6_96 x6_97 x6_98 x6_99 y6_97 y6_99 x7_17 x7_19 y7_16 y7_17 y7_18 y7_19 x7_40 x7_41 x7_42 x7_43 y7_41 y7_43 x7_73 x7_75 y7_73 y7_75 x7_97 x7_99 y7_97 y7_99 x8_73 x8_75 y8_72 y8_73 y8_74 y8_75 x8_121 x8_123 y8_120 y8_121 y8_122 y8_123 x9_25 x9_27 y9_25 y9_27 x9_49 x9_51 y9_48 y9_50 x9_97 x9_99 y9_97 y9_99 x9_104 x9_105 x9_106 x9_107 y9_105 y9_107 x10_16 x10_18 y10_16 y10_17 y10_18 x10_25 x10_27 y10_25 y10_27 x10_33 x10_35 y10_33 y10_35 x10_65 x10_67 y10_64 y10_65 y10_66 y10_67 x11_1 x11_3 y11_0 y11_2 y11_3 x11_9 x11_11 y11_8 y11_9 y11_10 y11_11 x11_33 x11_35 y11_32 y11_34 y11_35 x11_48 x11_50 x11_51 y11_49 y11_51 x11_56 x11_57 x11_58 x11_59 y11_57 y11_59 x11_88 x11_89 x11_90 x11_91 y11_88 y11_89 y11_90 y11_91 x11_105 x11_107 y11_105 y11_107 x12_8 x12_10 x12_11 y12_9 y12_11 x12_24 x12_26 x12_27 y12_25 y12_27 x12_41 x12_43 y12_40 y12_42 y12_43 x12_56 x12_57 x12_58 x12_59 y12_56 y12_57 y12_58 y12_59 x12_65 x12_67 y12_65 y12_67 x12_97 x12_99 y12_96 y12_98 x12_105 x12_107 y12_105 y12_107 x12_113 x12_115 y12_113 y12_115 x13_8 x13_9 x13_10 x13_11 y13_9 y13_11 x13_33 x13_35 y13_32 y13_33 y13_34 y13_35 x13_65 x13_67 y13_64 y13_66 y13_67 x13_72 x13_74 y13_73 y13_75 x13_113 x13_115 y13_113 y13_115 x14_17 x14_19 y14_16 y14_18 y14_19 x14_49 x14_51 y14_49 y14_51 x14_65 x14_67 y14_64 y14_66 x14_81 x14_83 y14_81 y14_83 x14_104 x14_106 x14_107 y14_105 y14_107 x15_24 x15_26 y15_25 y15_27 x15_48 x15_50 x15_51 y15_49 y15_51 x15_89 x15_91 y15_89 y15_91 x16_1 x16_3 y16_1 y16_3 x16_56 x16_58 x16_59 y16_57 y16_59 x17_0 x17_2 x17_3 y17_0 y17_1 y17_2 x17_25 x17_27 y17_24 y17_26 y17_27 x17_104 x17_106 y17_104 y17_105 y17_106 v0_40 x0_4 v0_42 x0_6 v0_48 x0_20 v0_50 x0_22 u0_16 u0_17 u0_18 u0_19 x1_28 x1_29 x1_30 x1_31 v0_52 x0_28 v0_54 x0_30 v0_16 v0_17 v0_18 v0_19 u0_20 v0_20 u0_21 v0_21 u0_22 v0_22 u0_23 v0_23 x1_61 x1_63 v0_28 v0_29 v0_30 v0_31 x0_84 x0_85 x0_86 x0_87 u0_40 u0_42 u0_48 u0_50 x1_93 x1_95 x0_92 x0_93 x0_94 x0_95 x0_108 x0_109 x0_110 x0_111 x1_117 x1_119 v1_5 v1_7 v1_52 v1_53 v1_54 v1_55 u1_21 v1_21 u1_23 v1_23 x2_60 x2_61 x2_62 x2_63 u1_33 v1_33 u1_35 v1_35 x2_108 x2_110 u2_28 u2_30 x3_13 x3_15 v2_4 v2_5 v2_6 v2_7 v2_28 v2_30 u2_33 u2_35 x3_108 x3_109 x3_110 x3_111 u3_28 u3_29 u3_30 u3_31 x4_12 x4_13 x4_14 x4_15 v3_45 v3_47 v3_28 v3_29 v3_30 v3_31 u3_45 u3_47 x4_69 x4_71 v4_44 v4_45 v4_46 v4_47 v4_9 v4_11 u5_25 u5_27 x6_21 x6_23 u5_48 u5_49 u5_50 u5_51 x6_92 x6_93 x6_94 x6_95 v6_49 v6_51 u6_9 u6_11 v6_20 v6_21 v6_22 v6_23 x7_53 x7_55 u6_37 u6_39 x7_100 x7_101 x7_102 x7_103 u7_1 v7_1 u7_3 v7_3 u7_24 u7_25 u7_26 u7_27 x8_21 x8_23 x8_44 x8_45 x8_46 x8_47 v7_24 v7_25 v7_26 v7_27 u7_61 u7_63 x8_77 x8_79 u7_37 u7_39 x8_101 x8_103 v8_49 v8_51 v8_13 v8_15 v8_60 v8_61 v8_62 v8_63 v8_25 v8_27 u8_60 u8_61 u8_62 u8_63 x9_77 x9_79 u8_52 u8_53 u8_54 u8_55 x9_125 x9_127 u9_8 u9_10 u9_17 u9_19 x10_29 x10_31 v9_13 v9_15 x10_53 x10_55 u9_33 u9_35 u9_37 v9_37 u9_39 v9_39 x10_101 x10_103 x10_108 x10_109 x10_110 x10_111 v10_1 v10_3 u10_5 u10_7 u10_24 u10_25 u10_26 x11_20 x11_22 u10_17 u10_19 x11_29 x11_31 v10_53 v10_55 x11_37 x11_39 v10_25 v10_27 v10_28 v10_29 v10_30 v10_31 u10_44 u10_45 u10_46 u10_47 x11_69 x11_71 u11_12 u11_14 u11_15 x12_5 x12_7 u11_28 u11_29 u11_30 u11_31 x12_13 x12_15 u11_4 u11_6 u11_7 v11_48 v11_50 u11_9 v11_9 u11_11 v11_11 v11_53 v11_55 x12_37 x12_39 v11_57 v11_59 u11_21 u11_23 x12_52 x12_54 x12_55 x12_60 x12_61 x12_62 x12_63 u11_33 u11_35 u11_48 u11_49 u11_50 u11_51 x12_92 x12_93 x12_94 x12_95 x12_109 x12_111 v12_41 v12_43 u12_0 v12_0 u12_2 v12_2 u12_3 v12_3 u12_29 u12_31 x13_12 x13_14 x13_15 v12_45 v12_47 v12_4 v12_5 v12_6 v12_7 u12_17 u12_19 x13_28 x13_30 x13_31 v12_57 v12_59 x13_45 x13_47 u12_20 v12_20 u12_21 v12_21 u12_22 v12_22 u12_23 v12_23 x13_60 x13_61 x13_62 x13_63 v12_29 v12_31 u12_45 u12_47 x13_69 x13_71 u12_33 u12_35 u12_36 u12_38 u12_41 u12_43 x13_101 x13_103 x13_109 x13_111 x13_117 x13_119 u13_29 u13_31 x14_12 x14_13 x14_14 x14_15 v13_44 v13_46 v13_47 u13_4 v13_4 u13_5 v13_5 u13_6 v13_6 u13_7 v13_7 v13_9 v13_11 v13_52 v13_54 v13_55 x14_37 x14_39 v13_61 v13_63 v13_25 v13_27 v13_29 v13_31 u13_44 u13_46 u13_47 x14_69 x14_71 v13_33 v13_35 u13_61 u13_63 x14_76 x14_78 u13_41 u13_43 x14_117 x14_119 v14_44 v14_45 v14_46 v14_47 u14_24 u14_26 u14_27 x15_21 x15_23 u14_9 v14_9 u14_11 v14_11 v14_12 v14_14 v14_57 v14_59 x15_53 x15_55 u14_44 u14_46 x15_69 x15_71 u14_33 v14_33 u14_35 v14_35 u14_57 u14_59 x15_85 x15_87 x15_108 x15_110 x15_111 v15_1 v15_3 v15_49 v15_51 u15_9 v15_9 u15_11 v15_11 u15_17 u15_19 x16_28 x16_30 v15_17 v15_19 x16_52 x16_54 x16_55 v15_28 v15_30 v15_31 u15_49 u15_51 x16_93 x16_95 u16_13 u16_15 x17_5 x17_7 v16_0 v16_2 v16_3 v16_52 v16_54 u16_21 v16_21 u16_23 v16_23 x17_60 x17_62 x17_63 u17_12 u17_13 u17_14 x18_4 x18_6 x18_7 v17_41 v17_43 v17_4 x18_8 v17_6 x18_10 v17_7 x18_11 u17_16 u17_18 u17_19 x18_29 x18_31 x18_24 x18_25 x18_26 x18_32 x18_34 x18_35 u17_32 x18_64 u17_33 x18_65 u17_34 x18_66 x18_81 x18_83 x18_108 x18_110 
```

* This output can be converted into the differential characteristics using _print_diff_characteristic.py_

## Print differential characteristics

* Differential characteristics can be printed using _print_diff_characteristic.py_
* There are two argument for _print_diff_characteristic.py_. First argument is _WARP_Result_18.txt_ and second argument is the characteristic number in _WARP_Result_18.txt_.
* The differential characteristic for 18-round PIPO is printed using following command:\
```print_diff_characteristic.py WARP_Result_18.txt 1```
* The output is in the following format:
```
Differential Probability for 18 rounds of WARP_128 is 2^{-122.0} :: Total No. of Active S-Box => 61
The input difference of the round 0 is: 
0000  0000  0000  1010  1111  0000  0000  0000  1111  1010  1111  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  0000  0101  1111  0101  0000  0000  0000  0101  0000  :: Hex => 000a  f000  faf0  0000  0a00  0000  5f50  0050   :: 0x000af000faf000000a0000005f500050 :: Probability => 2^{-0} :: No. of Active S-Box => 0

The input difference of the round 1 is: 
0000  0000  1010  0000  0000  0101  0000  0000  1010  0000  0000  0000  0000  0000  0000  0000  1010  1111  0000  0000  0000  0000  0000  0000  1111  0000  0000  0000  0000  0000  0000  0000  :: Hex => 00a0  0500  a000  0000  af00  0000  f000  0000   :: 0x00a00500a0000000af000000f0000000 :: Probability => 2^{-8} :: No. of Active S-Box => 4

The input difference of the round 2 is: 
0000  0000  0000  0000  0101  1111  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1111  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1010  0000  0000  :: Hex => 0000  5f00  0000  0000  f000  0000  0000  0a00   :: 0x00005f0000000000f000000000000a00 :: Probability => 2^{-4} :: No. of Active S-Box => 2

The input difference of the round 3 is: 
0000  0000  0000  0000  1111  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1010  1111  0000  0000  :: Hex => 0000  f000  0000  000a  0000  0000  0000  af00   :: 0x0000f0000000000a000000000000af00 :: Probability => 2^{-4} :: No. of Active S-Box => 2

The input difference of the round 4 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1111  0000  0000  0000  :: Hex => 0000  0000  0000  00a0  0000  0000  0000  f000   :: 0x00000000000000a0000000000000f000 :: Probability => 2^{-4} :: No. of Active S-Box => 2

The input difference of the round 5 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  1111  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  :: Hex => 0000  0000  0f00  0000  0000  0000  000a  0000   :: 0x000000000f00000000000000000a0000 :: Probability => 2^{-0} :: No. of Active S-Box => 0

The input difference of the round 6 is: 
0000  0000  0000  0000  0000  0000  0000  1111  1111  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  :: Hex => 0000  000f  f000  0000  000a  0000  00a0  0000   :: 0x0000000ff0000000000a000000a00000 :: Probability => 2^{-4} :: No. of Active S-Box => 2

The input difference of the round 7 is: 
0000  0000  0000  0000  0000  0000  1111  1010  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  1010  0000  0000  1111  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  :: Hex => 0000  00fa  0000  0a00  00a0  0f00  000a  0000   :: 0x000000fa00000a0000a00f00000a0000 :: Probability => 2^{-4} :: No. of Active S-Box => 2

The input difference of the round 8 is: 
0000  1010  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  1010  1010  0000  0000  0000  0000  0000  0000  1111  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  :: Hex => 0a00  00a0  0000  aa00  0000  f000  00a0  0000   :: 0x0a0000a00000aa000000f00000a00000 :: Probability => 2^{-8} :: No. of Active S-Box => 4

The input difference of the round 9 is: 
1010  0000  0000  0000  0000  1111  0000  1010  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  0000  :: Hex => a000  0f0a  0000  a000  000a  0000  0a00  0000   :: 0xa0000f0a0000a000000a00000a000000 :: Probability => 2^{-4} :: No. of Active S-Box => 2

The input difference of the round 10 is: 
0000  0000  0000  0000  1111  0000  1010  0000  0000  0000  0000  0000  0000  0000  0000  1010  0000  0000  1010  0000  0000  0000  0000  1010  1010  1010  0000  0101  0000  0000  0000  0000  :: Hex => 0000  f0a0  0000  000a  00a0  000a  aa05  0000   :: 0x0000f0a00000000a00a0000aaa050000 :: Probability => 2^{-8} :: No. of Active S-Box => 4

The input difference of the round 11 is: 
0000  0000  0000  0000  0000  1010  0000  0000  0000  1111  0000  0000  0000  0000  1010  0000  0000  1111  0000  1101  0000  0000  1010  1010  1010  0000  0101  0000  0000  1010  0000  1010  :: Hex => 0000  0a00  0f00  00a0  0f0d  00aa  a050  0a0a   :: 0x00000a000f0000a00f0d00aaa0500a0a :: Probability => 2^{-8} :: No. of Active S-Box => 4

The input difference of the round 12 is: 
0000  0000  0000  1010  1010  1010  0000  1010  1111  0000  0000  0000  0000  0000  0000  1010  1111  1111  1101  0000  0000  1010  1010  0000  0000  1101  0000  0000  1010  1101  1010  0000  :: Hex => 000a  aa0a  f000  000a  ffd0  0aa0  0d00  ada0   :: 0x000aaa0af000000affd00aa00d00ada0 :: Probability => 2^{-14} :: No. of Active S-Box => 7

The input difference of the round 13 is: 
0000  0000  1010  1010  1010  0000  1010  0000  0000  0000  0000  0000  0000  0101  1010  1010  1111  0000  0000  0000  1010  0000  0000  1010  1101  0000  0000  0000  1101  1111  0000  0000  :: Hex => 00aa  a0a0  0000  05aa  f000  a00a  d000  df00   :: 0x00aaa0a0000005aaf000a00ad000df00 :: Probability => 2^{-16} :: No. of Active S-Box => 8

The input difference of the round 14 is: 
0000  0000  1010  0000  0000  1101  0000  0000  0000  0000  0000  1010  0101  0000  1010  1010  0000  0000  0000  1010  0000  0000  1010  0000  0000  0000  0000  1010  1111  0000  0000  0000  :: Hex => 00a0  0d00  000a  50aa  000a  00a0  000a  f000   :: 0x00a00d00000a50aa000a00a0000af000 :: Probability => 2^{-10} :: No. of Active S-Box => 5

The input difference of the round 15 is: 
0000  0000  0000  0000  1101  0000  0000  0000  0000  1010  1010  0000  0000  0000  1010  0000  0000  0000  1010  1101  0000  0000  0000  0000  0000  0101  1010  0000  0000  0000  0000  0000  :: Hex => 0000  d000  0aa0  00a0  00ad  0000  05a0  0000   :: 0x0000d0000aa000a000ad000005a00000 :: Probability => 2^{-10} :: No. of Active S-Box => 5

The input difference of the round 16 is: 
0000  0000  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  0000  0000  0000  0000  1101  1101  0000  0000  0000  0000  0000  0101  0000  0000  0000  0000  0000  0000  1010  :: Hex => 0000  0000  a000  0000  0dd0  0000  5000  000a   :: 0x00000000a00000000dd000005000000a :: Probability => 2^{-6} :: No. of Active S-Box => 3

The input difference of the round 17 is: 
0000  0000  0000  0000  0000  0101  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1101  0000  0000  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0000  1010  1101  :: Hex => 0000  0500  0000  0000  d000  0000  0a00  00ad   :: 0x0000050000000000d00000000a0000ad :: Probability => 2^{-4} :: No. of Active S-Box => 2

The input difference of the round 18 is: 
0000  0000  0000  0000  0101  0000  0000  0000  0000  0000  0000  1010  0000  0000  0000  0111  0000  0000  0000  0000  0000  0000  0000  1101  1010  0111  0000  0000  0000  1101  1101  0000  :: Hex => 0000  5000  000a  0007  0000  000d  a700  0dd0   :: 0x00005000000a00070000000da7000dd0 :: Probability => 2^{-6} :: No. of Active S-Box => 3

```
## Acknowledgement 
1. https://github.com/zhuby12/MILP-basedModel

