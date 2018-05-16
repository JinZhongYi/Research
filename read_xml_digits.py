# Author:金中一
# Date:2018/4/24
# Version:1.0
# Revisited
# Date:2018/5/16
# Version:2.0
# Name:单个ECG_xml文件中12导联数据的读取并保存txt/mat文件
# Input:
#   xml_url：xml文件路径
#   save_url:输出文件保存路径
#   file_type:选择保存文件格式txt/mat
#Output:
#   编号为1，2，3.。。的txt文件是原始xml中的digits的str类型文件无法直接用
#   编号为V1,V2,V3。。。的txt/mat文件是处理过后的N*1的数据
#Attenation:如果要批量处理xml文件，先查找出所有xml文件路径，再批量新建文件夹存入数组，然后循环调用就行

import scipy.io
import xml.dom.minidom
import os
import threading

#写入控制
def write(save_url,file_type,i):
    f=open(save_url+'\%d.txt'%i,'r')#在save_url路径下创建一个txt文件
    line=f.readline()
    lines=line.strip().split(' ')#以空格为分隔符分割读取到的文件，原始xml文件都出来是str类型
    #依次存入data数组中
    data=[]
    for i2 in range(0,len(lines)):
        j=float(lines[i2])
        data.append(j)
    #print(type(data[i2]))
    f.close()

    #按照需求将data文件存成不同类型文件
    if file_type=='mat':
        scipy.io.savemat(save_url+'\V%d.mat'%i,{'A':data})
    elif file_type=='txt':
        f=open(save_url+'\V%d.txt'%i,'w')
        for d in data:
            f.write(str(d)+'\r\n')#write只能写入str型数据
        f.close()

#读取xml文件中的12导联信息
def read_xml_digits(xml_url,save_url,file_type):
    i=1
    xml_tree=xml.dom.minidom.parse(xml_url)#读取xml树状结构
    root=xml_tree.documentElement#获取根节点
    digits=root.getElementsByTagName('digits')#获取digits标签下的信息，一共12个
    for digit in digits:
        data=digit.childNodes[0].data#得到每个digits标签下的导联信息，因为digits只有一个子节点
        #写入str型的导联信息
        new_save_url=save_url+'\%d.txt'%i
        f=open(new_save_url,'w')
        f.write(data)
        f.close()
        write(save_url,file_type,i)
        os.remove(new_save_url)#删除write函数执行的过渡文件
        i=i+1

#批量读写操作
def Doit(save_url,file_type,url):
    #os.walk会遍历文件夹下所有的文件与文件夹以及子文件夹下的文件，并返回一个元祖，该函数没有返回值，topdowm则是控制先读文件还是先都文件夹的顺序关系
    #os.walk读取会有一个怪象，排序不按照大小排序，例如：文件名为1到200,files排序是1,10,100,101,102..109,11,110,111
    #所以要值得注意
    for root, dirs, files in os.walk(url, topdown=False):
        for name in files:
            names = name.strip().split('.')
            print(names)
            xml_url = os.path.join(root, name)
            new_save_url = os.path.join(save_url, names[0])
            folder = os.path.exists(new_save_url)
            if not folder:#创建目录
                os.makedirs(new_save_url)
            read_xml_digits(xml_url, new_save_url, file_type)


save_url=r'C:\Users\xxxjz\Desktop\1112'#需要保存的文件夹地址
file_type='mat'
url=r'C:\Users\xxxjz\Desktop\data1-943\data1-251'#需要遍历的文件夹地址
url1=r'C:\Users\xxxjz\Desktop\data1-943\data252-540'
url2=r'C:\Users\xxxjz\Desktop\data1-943\data541-943'
t0=threading.Thread(target=Doit,args=(save_url,file_type,url))
t1=threading.Thread(target=Doit,args=(save_url,file_type,url1))
t2=threading.Thread(target=Doit,args=(save_url,file_type,url2))
t0.start()
t1.start()
t2.start()
t0.join()
t1.join()
t2.join()
# xml_url=r'G:\降噪\20180419\1.xml'
# save_url=r'C:\Users\xxxjz\Desktop\123'

# read_xml_digits(xml_url,save_url,file_type)