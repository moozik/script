#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''
p(a|b)=p(a)p(b|a)/p(b)

转为数组
np.array(df[:1]).tolist()[0]
'''

import pandas as pd
import numpy as np
import re
#完整数据
df = pd.read_csv('C:/Users/v_wangyusen_dxm/Desktop/tongdao/some-code/Bayes/adult/adult.txt',header=None)
#待预测数据
df_test = pd.read_csv('C:/Users/v_wangyusen_dxm/Desktop/tongdao/some-code/Bayes/adult/adult_test.txt',header=None)

#数据条数
data_count = len(df)

columns_en = ["age","work_type","college","marry","job","family_role","color","sex","in",
"out","work_time","country","rich"]
columns_cn = ["年龄","工作类型","教育程度","婚姻状态","职业","家庭角色","种族","性别","资本收益",
"资本损失","工作时长","原国家","年收入"]
df.columns = columns_en
df_test.solumns = columns_en[:-1]

columns = {
"age":['0-18','19-20','21-22','23-23','24-25','25-26','27-29','30-32','33-35','36-39','40-43','44-47','48-51','52-60','61-100'],
"work_type":['Private','Self-emp-not-inc','Self-emp-inc','Federal-gov','Local-gov','State-gov','Without-pay','Never-worked'],
"college":['Bachelors','Some-college','11th','HS-grad','Prof-school','Assoc-acdm','Assoc-voc','9th','7th-8th','12th','Masters','1st-4th','10th','Doctorate','5th-6th','Preschool'],
"marry":['Married-civ-spouse','Divorced','Never-married','Separated','Widowed','Married-spouse-absent','Married-AF-spouse'],
"job":['Tech-support','Craft-repair','Other-service','Sales','Exec-managerial','Prof-specialty','Handlers-cleaners','Machine-op-inspct','Adm-clerical','Farming-fishing','Transport-moving','Priv-house-serv','Protective-serv','Armed-Forces'],
"family_role":['Wife','Own-child','Husband','Not-in-family','Other-relative','Unmarried'],
"color":['White','Asian-Pac-Islander','Amer-Indian-Eskimo','Other','Black'],
"sex":['Female','Male'],
"in":['==0','1-1000','1001-2000','2001-3000','3001-4000','4001-5000','>5000'],
"out":['==0','1-1000','1001-2000','2001-3000','3001-4000','4001-5000','>5000'],
"work_time":['==0','1-10','11-20','21-30','31-39','==40','41-50','51-60','61-99'],
"country":['United-States','Cambodia','England','Puerto-Rico','Canada','Germany','Outlying-US','Guam-USVI-etc','India','Japan','Greece','South','China','Cuba','Iran','Honduras','Philippines','Italy','Poland','Jamaica','Vietnam','Mexico','Portugal','Ireland','France','Dominican-Republic','Laos','Ecuador','Taiwan','Haiti','Columbia','Hungary','Guatemala','Nicaragua','Scotland','Thailand','Yugoslavia','El-Salvador','Trinadad&Tobago','Peru','Hong','Holand-Netherlands'],
"rich":[1,0],
}

#数字范围的列

columns_sum = {}


# print(df.head(5))
number_range_list = ["age","in","out","work_time"]

reg_renge = '(^>|^<|^==|^\d+)-?(\d+)'

reg_renge_1 = '^(\d+)-(\d+)$'
reg_renge_2 = '^==(\d+)$'
reg_renge_3 = '^>(\d+)$'
reg_renge_4 = '^<(\d+)$'

#统计各列总数
for flag in columns['rich']:
    columns_sum[flag] = {}
    fenmu = len(df[(df['rich'] == flag)])
    for key in  columns:
        if key in number_range_list:
            #数字数据
            for range_text in columns[key]:
                reg_res = re.findall(reg_renge,range_text)[0]
                if reg_res == []:
                    continue

                if '==' == reg_res[0]:
                    columns_sum[flag][key + '_' + range_text] = len(df[(df['rich'] == flag) & (df[key] == int(reg_res[1]))]) / fenmu
                if '>' == reg_res[0]:
                    columns_sum[flag][key + '_' + range_text] = len(df[(df['rich'] == flag) & (df[key] > int(reg_res[1]))]) / fenmu
                if '<' == reg_res[0]:
                    columns_sum[flag][key + '_' + range_text] = len(df[(df['rich'] == flag) & (df[key] < int(reg_res[1]))]) / fenmu
                if re.match('\d+',reg_res[0]):
                    columns_sum[flag][key + '_' + range_text] = len(df[(df['rich'] == flag) & (int(reg_res[0]) <= df[key]) & (df[key] <= int(reg_res[1]))]) / fenmu
        else:
            #枚举数据
            for item in columns[key]:
                columns_sum[flag][item] = len(df[(df[key] == item) & (df['rich'] == flag)]) / fenmu
#计算整体papb
count_a = len(df[(df['rich'] == 1)])
count_b = len(df[(df['rich'] == 0)])
pa_value = count_a/(count_a + count_b)
pb_value = count_b/(count_a + count_b)


print(columns_sum)

print(pa_value,pb_value)

#计算结果
def calc_papb(columns_sum, row_data):
    #[x for x in list(columns_sum[pa_val]) if x != pa_val][0]

    pa_val = 1
    pb_val = 0
    
    col_dict = {
        0:'age',
        8:'in',
        9:'out',
        10:'work_time',
    }
    
    res_a = 1
    res_b = 1
    
    return_arr = []
    for i in range(len(row_data)):
        col = row_data[i]
        # print('\n','*'*3,i,col)
        if col == '?':
            return_arr.append(1)
            continue
        if i in [0,8,9,10]:
            key = col_dict[i]
            for range_text in columns[key]:
                reg_res = re.findall(reg_renge,range_text)[0]
                # print(key, range_text, reg_res)
                if '==' == reg_res[0] and col == int(reg_res[1]):
                    col = key + '_' + range_text
                    break
                else:
                    pass
                    # print('!check','==' == reg_res[0],col == int(reg_res[1]))
                
                if '>' == reg_res[0] and int(col) > int(reg_res[1]):
                    col = key + '_' + range_text
                    break
                else:
                    pass
                    # print('!check','>' == reg_res[0],col > int(reg_res[1]))
                
                if '<' == reg_res[0] and int(col) < int(reg_res[1]):
                    col = key + '_' + range_text
                    break
                else:
                    pass
                    # print('!check','<' == reg_res[0],col < int(reg_res[1]))
                
                if re.match('\d+',reg_res[0]) and int(col) >= int(reg_res[0]) and int(col) <= int(reg_res[1]):
                    col = key + '_' + range_text
                    break
                else:
                    pass
                    # print('!check', reg_res[0], reg_res[1], col)
        else:
            if col not in columns_sum[pa_val]:
                continue

        res_a *= columns_sum[pa_val][col]
        res_b *= columns_sum[pb_val][col]
    
    res_a *= pa_value
    res_b *= pb_value
    
    result_a = res_a/(res_a + res_b)
    # result_b = res_b/(res_a + res_b)
    result_c = 1 - result_a
    # return result_a, result_c
    if result_a > result_c:
        return '1'
    else:
        return '0'

'''
df_list = np.array(df_test[:1]).tolist()[0]
print(df_list)
result = calc_papb(columns_sum, data_count,df_list)
print(result)
'''


'''
result = ''
result2 = ''
for row in np.array(df[:1000]).tolist():
    # result += '{0[0]},{0[1]}\n'.format(calc_papb(columns_sum, row))
    tmp = calc_papb(columns_sum, row[:-1])
    if tmp == str(row[-1:][0]):
        result += '{},成功\n'.format(','.join([str(x) for x in row]))
    else:
        result2 += '{},失败\n'.format(','.join([str(x) for x in row]))

file = open('d:/res.txt','w')
file.write(result+result2)
file.close()
'''
result = ''
for row in np.array(df_test).tolist():
    # result += '{0[0]},{0[1]}\n'.format(calc_papb(columns_sum, row))
    result += calc_papb(columns_sum, row)



# print(result)

file = open('d:/res.txt','w')
file.write(result)
file.close()