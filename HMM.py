import argparse
import sys
import numpy as np


pro_file='example.hmm'
test_file='example.fa'


with open(pro_file) as f:
    lines = f.readlines()
    Pi = np.array([float(i) for i in lines[1].split(' ')])  #初始状态概率矩阵

    temp=[]
    for line in lines:
        line=line.split()
        temp.append(line)

temp1 = temp[2]
temp2 = temp[3]

A = [list(map(float,temp1))[0:2], list(map(float,temp2))[0:2]]#转移概率矩阵
B = [list(map(float,temp1))[2:6], list(map(float,temp2))[2:6]]#观测概率矩阵

A = np.log2(A)
B = np.log2(B)
Pi = np.log2(Pi)



def transform(letters):
    number_list = []
    for case in list(letters):
        if case == 'A':
            number_list.append(0)
        elif case== 'C':
            number_list.append(1)
        elif case == 'G':
            number_list.append(2)
        elif case == 'T':
            number_list.append(3)
        elif case == 'a':
            number_list.append(0)
        elif case == 'c':
            number_list.append(1)
        elif case == 'g':
            number_list.append(2)
        elif case == 't':
            number_list.append(3)

    return number_list

def read(test_file):
    with open(test_file, 'r') as f:
        next(f)  # 跳过第一行
        lines = f.readlines()
        test_list = []
        for line in lines:
            line = line.strip().split('\t')
            test_list.append(line)

        test_list = [x[0] for x in test_list]
        number_list = []
        for case in test_list:
            number_list.append(transform(case))

    return number_list


if __name__ == "__main__":
    pi = len(Pi)  # state的个数，这里为2

    # 状态列表
    state_0 = []
    state_1 = []
    state = [state_0, state_1]

    # 导入初始概率
    initial_0 = Pi[0]
    initial_1 = Pi[1]
    pro_sum = [initial_0 , initial_1]
    temp = [initial_0 , initial_1]

    fa_list = read(test_file)
    for m in range(len(fa_list)):
        for n in range(len(fa_list[m])):
            fa_num = fa_list[m][n]
            if m + n  == 0:
                pro_sum[0] = pro_sum[0] + B[0][fa_num]
                pro_sum[1] = pro_sum[1] + B[1][fa_num]
            else:
                for i in range(2):
                    pro_sum0 = pro_sum[0] + A[0][i] + B[i][fa_num]
                    pro_sum1 = pro_sum[1] + A[1][i] + B[i][fa_num]
                    if pro_sum0 > pro_sum1:
                        state[i].append(0)
                        temp[i] = pro_sum0
                    else:
                        state[i].append(1)
                        temp[i] = pro_sum1

                pro_sum[0] = temp[0]
                pro_sum[1] = temp[1]

#比较最后的两个state哪个大
start=int(pro_sum[1]<pro_sum[0])

length=len(state[start])
true_path=[]
true_path.append(state[start][length-1])

for i in range(length):
    j=length-i-1
    if  j ==length-1:
        r=state[start][j]
    else:
        r = state[r][j]
        true_path.append(state[r][j - 1])

true_path=list(reversed(true_path))

j=1

for i in range(1,len(true_path)):
    if (true_path[i]!= true_path[i-1]):
            print('From '+str(j)+' to '+str(i-1)+' is state '+str(true_path[i-1]+1))
            j=i
    if (i==len(true_path)-1):
        print('From ' + str(j) + ' to ' + str(length+1) + ' is state ' + str(true_path[start] + 1))



























