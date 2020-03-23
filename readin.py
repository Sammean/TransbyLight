import struct
import os
if __name__ == '__main__':
    filepath='  '//filename
    binfile = open(filepath, 'rb') #打开二进制文件
    size = os.path.getsize(filepath) #获得文件大小
    flag=0#记录
    a=0#记录余数
    b=0#
    list1=[]#建立空列表，利用列表记录二进制数据
    list2=[]#建立空列表，逆序储存，方便转化
    for i in range(size):
        data = binfile.read(1) #每次输出一个字节
        num=struct.unpack('B',data)#转化成十进制
        for j in range(4)://转化成二进制
             list2.append(num%2)
             num/=2
        for h in range(4):
             list1.append(list2[3-i])
    list2.clear()#清除list2的数据
    binfile.close()