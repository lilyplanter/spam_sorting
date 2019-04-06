# -*- coding: utf-8 -*-
"""
Created on Sun May 19 18:54:36 2013

@author: rk
"""
import nltk
import os
import math
root=os.getcwd()
train_data =os.path.join(root+"/data set/hw1_data/train/")
test_data =os.path.join(root+"/data set/hw1_data/test/")
ham = "ham/"
spam = "spam/"
MAX_NUM = 5000 
K = 2
#把词典按照每个词的出现顺序按从大到小排序
def sort_by_value(d):
    #lambda作为一个表达式，定义了一个匿名函数;
    #cmp(x,y) 函数用于比较2个对象，如果 x < y 返回 -1, 如果 x == y 返回 0, 如果 x > y 返回 1.这里表示按照元组的第二个元素进行比较（即按value比）
    sortedd=sorted(d.items(),key=lambda a:a[1], reverse = True)
    return sortedd
    

#处理单词，删去单词中的空白符，并把所有的大写转小写
def word_process(word):
    word_low = word.strip().lower()
    word_final = word_low
    return word_final

def add_to_dict(word, dict_name):
    if(word in dict_name):
        num = dict_name[word]
        num += 1
        dict_name[word] = num
    else:
        dict_name[word] = 1
#排除那些出现过多和出现过少的词,在返回的词典中，只有dictionary中出现过多或过少的词
def negative_dict_maker(dictionary):
    d = dict()
    for (key, value) in dictionary.items():
        if(value >= MAX_NUM or value <= 1):       
            d[key]=1
    return d

def text_reader(file_name, dict_name):
    tokenizer = nltk.RegexpTokenizer("[\w']{3,}")   #leave the word with length > 1
    f = open(file_name, 'r')
    for line in f:
        words = tokenizer.tokenize(line)
        for word in words:
            word = word_process(word)
            add_to_dict(word, dict_name)#把词加入词典
    f.close()

def save_dict(dict_name, file_path, all_flag):
    f = open(file_path, 'w')#"dict_file.data", 'w')
    word_max = ""#记录出现最多的单词
    value_max = 0;#记录出现最多的单词出现的次数
    for (key, value) in dict_name.items():
        if(not all_flag):
            if value > 1 and value < MAX_NUM:
                f.writelines(key+" "+str(value)+"\n")
            if value > value_max:
                word_max = key
                value_max = value
        else:
            f.writelines(key+" "+str(value)+"\n")
            if value > value_max:
                word_max = key
                value_max = value
    f.close()
    print("Save_dict-----> Max_key:"+word_max+", Max_value:"+str(value_max))
        
def load_dict(file_path):
    dict_loaded = dict()
    f = open(file_path, 'r')
    
    while 1:
        line = f.readline()
        if not line:
            break
        words = line.split()
        dict_loaded[words[0]] = int(words[1])
    f.close()
    return dict_loaded
#把正常邮件数目，垃圾邮件数目，总数目存储在一个data文件中
def save_file_number(ham, spam, total):
    f = open("file_number.data", 'w')
    f.writelines(str(ham)+"\n")
    f.writelines(str(spam)+"\n")
    f.writelines(str(total)+"\n")
    f.close()

#make the master dictionary and calculate the number of ham or spam
def traverse_dictionary_maker(file_path):
    dictionary = dict()
    ham_path = file_path+ham
    spam_path = file_path+spam
    path = {ham_path,spam_path}
    path_order = 0
    num_ham = 0
    num_spam = 0
    for i in path:#从正常邮件文件夹到垃圾邮件文件夹
        folders = os.listdir(i)#获得文件夹下所有的文件名称
        for file_name in folders:
            if os.path.isfile(i+file_name):#对于那些是文件的文件名
                text_reader(i+file_name, dictionary)#把邮件里的词加入词典
                if(path_order == 0):
                    num_ham += 1#记录正常邮件数量
                else:
                    num_spam += 1#记录垃圾邮件数量
        path_order += 1
    #initialize
    save_file_number(num_ham, num_spam, num_ham + num_spam)#保存训练集的数量信息
    return dictionary

#构造垃圾邮件/正常邮件词典
def dict_creator(file_path,negative_dict):
    dictionary = load_dict("dict_file.data")#读取未优化的总词典
    for key in dictionary:#把总词典中每个单词的出现次数都记为0
        dictionary[key] = 0
    if(not os.path.isfile(file_path)): #如果路径不是指向单个文件而是文件夹
        folders = os.listdir(file_path)#提取该文件夹下所有文件的文件名
        for file_name in folders:
            raw_dict = dict()
            if os.path.isfile(file_path+file_name):
                text_reader(file_path+file_name, raw_dict)
            for key in raw_dict:#对于那些出现在single词典中却不出现在垃圾词词典中的词               
                if key not in negative_dict:
                    num = dictionary[key]
                    num += 1
                    dictionary[key] = num
    else:
        raw_dict = dict()
        text_reader(file_path, raw_dict)
        for key in raw_dict:#对于那些出现在single词典中却不出现在垃圾词词典中的词               
            if key not in negative_dict:
                raw_dict[key]=1
        dictionary=raw_dict

    return dictionary
    

#读取之前存储的训练集（正常邮件数目，垃圾邮件数目，总数）
def read_w_number():
    f = open("file_number.data", 'r')
    lines = f.readlines()
    w_num = [int(lines[0]), int(lines[1]), int(lines[2])]
    f.close()
    return w_num

#输出字典的前20个词
def print_top_twenty(list_name):
    index = 0
    while(index < 20):
        print(list_name[index])
        index += 1

def calculate(word, dict_name, n_w, exist_flag):
    if(exist_flag):
        result = math.log(dict_name[word]+1)
    else:
        #print("n_w:"+str(n_w)+word)
        #print(str(dict_name[word]))
        result = math.log(n_w+K-dict_name[word])
    return result

def bayes_score(vector, dict_name, n_w):
    #print(str(n_w))
    result = 0.0
    for (key, value) in dict_name.items():
       exist_flag = (key in vector)
       result += calculate(key, dict_name, n_w, exist_flag)
       result -= math.log(n_w)
    return result
#计算file_path对应的邮件是否是垃圾邮件
def predict(file_path, w_num, ham_dict, spam_dict):
    #读取待测邮件并给其建立词典
    vector = dict_creator(file_path,negative_dict)
    
    prob_ham = bayes_score(vector, ham_dict, w_num[0])
    prob_spam = bayes_score(vector, spam_dict, w_num[1])
    if prob_ham > 1.15*prob_spam:
        return 0#正常邮件
    else :
        return 1#垃圾邮件
    

#folder_path =test_data+spam
#files = os.listdir(folder_path)
#for file in files:
#    print(file)
#    f = open("file.data", 'r',encoding='utf-8')
    
file_path = train_data
dictionary = traverse_dictionary_maker(file_path)
negative_dict = negative_dict_maker(dictionary) #过滤掉那些出现过多和过少的词
# print ("negative: "+str(len(negative_dict))) #39624
save_dict(dictionary, "dict_file.data", False)   #把词典存储在文件中
dictionary = load_dict("dict_file.data")
w_num = read_w_number() #读取训练集的数量信息
#==================================================================================#
print("训练集信息：")
print("正常邮件数目："+str(w_num[0])+"垃圾邮件数目："+str(w_num[1])+"邮件总数："+str(w_num[2]))#把读取的训练集的信息输出

#构建正常邮件词典并存储
ham_dict = dict_creator(train_data + ham, negative_dict)
save_dict(ham_dict, "ham_dict.data", True)
print("成功建立正常邮件词典！")
#构造垃圾邮件词典并存储
spam_dict = dict_creator(train_data + spam, negative_dict)
save_dict(spam_dict, "spam_dict.data", True)
print("成功建立垃圾邮件词典！")
#把正常邮件词典和垃圾邮件词典分别按从大到小进行排序并分别输出前20个词
print("正常邮件出现最多的前20个词：")
list_ham = sort_by_value(ham_dict)
print_top_twenty(list_ham)
print("-------------------------------------------")
print("正常邮件出现最多的前20个词：")
list_spam = sort_by_value(spam_dict)
print_top_twenty(list_spam)

def test(data_set):
    test_set = [ham, spam]
    #test_set = [spam, ham]
    correctrate=0;
    testnum=0
    for w in test_set:
        correctnum=0
        folder_path = data_set + w 
        print (folder_path)
        files = os.listdir(folder_path)
        total_num = 0
        ham_predict_num = 0
        spam_predict_num = 0
        print(len(files))
        f = open("file.data", 'w')
        f.writelines(folder_path+"\n")#写入文件夹的路径
        for file in files:#遍历文件夹下的每一个文件
            if os.path.isfile(folder_path+file):#如果是文件的话
                f.writelines(folder_path+file+"\n")#写入文件的路径
                result = predict(folder_path+file, w_num, ham_dict, spam_dict)#计算分类结果   
                #更新测试的文件数目
                total_num += 1
                if(result == 0):
                    ham_predict_num += 1
                    if(w == ham):
                        correctnum+=1                  
                else:
                    spam_predict_num += 1
                    if (w == spam):
                        correctnum+=1
                        
        correctrate+=correctnum
        testnum+=total_num
        f.close()    
        print("邮件总数：" + str(total_num))
        print("被分类为正常邮件的邮件数" + str(ham_predict_num))
        print("被分类为垃圾邮件的邮件数" + str(spam_predict_num))
        print("分类正确率"+str(correctnum/total_num))
    print("总正确率："+str(correctrate/testnum))
print("测试开始！")
test(test_data) #对测试集进行测试



print("-------------ends------------------")




