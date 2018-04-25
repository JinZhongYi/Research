# Author:金中一
# Date:2018/4/24
# Version:1.0
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

#写入控制
def write(save_url,file_type,i):
    f=open(save_url+'\%d.txt'%i,'r')
    line=f.readline()
    lines=line.strip().split(' ')
    data=[]
    for i2 in range(0,len(lines)):
        j=float(lines[i2])
        data.append(j)
    #print(type(data[i2]))
    f.close()
    if file_type=='mat':
        scipy.io.savemat(save_url+'\V%d.mat'%i,{'A':data})
    elif file_type=='txt':
        f=open(save_url+'\V%d.txt'%i,'w')
        for d in data:
            f.write(str(d)+'\r\n')
        f.close()


def read_xml_digits(xml_url,save_url,file_type):
    i=1
    xml_tree=xml.dom.minidom.parse(xml_url)
    root=xml_tree.documentElement
    digits=root.getElementsByTagName('digits')
    for digit in digits:
        data=digit.childNodes[0].data
        f=open(save_url+'\%d.txt'%i,'w')
        f.write(data)
        f.close()
        write(save_url,file_type,i)
        i=i+1

xml_url=r'G:\降噪\20180419\1.xml'
save_url=r'C:\Users\xxxjz\Desktop\123'
file_type='txt'
read_xml_digits(xml_url,save_url,file_type)