from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt


##切割图片
def cropimg(imgname):
    img=Image.open("imgs_processed/"+imgname)
    w,h=img.size
    img.crop((0, 0, w, 26*1)).save("crops/%s-head.png" % imgname)
    for i in range(1,11):
        if(h<26*(i+1)):break
        img.crop((0,26*i,w,26*(i+1))).save("crops/%s-%d.png" % (imgname,i))
    print(w,h)

##获取图片2值化数据
def getimgdata(imgname):
    imgdata=np.array(Image.open("imgs/"+imgname))
    h,w=imgdata.shape[0:2]
    dstdata=np.zeros((h,w),dtype=np.int)
    for x in range(0,w):
        for y in range(0,h):
            if(x<2 or x>=w-2 or y<2 or y%26==0):    #左侧2列,上侧2行右侧2列设置为空白  ,每隔26行,这一行设置为空白
                dstdata[y,x]=0
            else:
                if(y<26):
                    if(imgdata[y,x,0]==0):  #如果是0表示黑色背景
                        dstdata[y,x]=0
                    else:
                        dstdata[y,x]=1
                else:
                    if(imgdata[y,x,0] in [192,255]):  #如果是这两种色,则设置为背景
                        dstdata[y,x]=0
                    else:
                        dstdata[y,x]=1
    return dstdata
    #############用plt查看下处理结果
    plt.figure("img")
    plt.imshow(dstdata)
    plt.show()
    ###############
#####################用2值化数据生成更易于识别的图片
def data2img(imgdata,imgname):
    dstname="imgs_processed/"+imgname
    if(os.path.isfile(dstname)):
        return
    h,w=imgdata.shape
    dstdata=np.zeros((h,w,3),dtype=np.uint8)
    for x in range(w):
        for y in range(h):
            if(imgdata[y,x]==1):
                dstdata[y,x,0]=0
                dstdata[y,x,1]=0
                dstdata[y,x,2]=0
            else:
                dstdata[y,x,0]=255
                dstdata[y,x,1]=255
                dstdata[y,x,2]=255

    print(imgname)
    img=Image.fromarray(dstdata,'RGB')
    img.save(dstname)

###########直接定义个变量存储识别模版
head_sample=[
    ["流水号",[3,7,12,12,9,6,10,9,5,14,14,5,10,12,6,4,5,1,0,2,2,3,4,5,6,4,3,17,16,3,5,5,5,5,4,2,1,0,1,1,1,1,8,11,5,5,5,6,6,6,13,12,2,1,1]]
    ,["评审分组(药品编码)",[1,2,5,13,10,3,4,6,6,5,17,16,3,5,5,5,3,1]]
]
body_sample=[

]
##############识别图片标题
def recogHead(imgdata):
    head=imgdata[:26,:]
    h,w=imgdata.shape
    hist=np.sum(head,axis=0)

    printflag=False
    x_start=0
    x_end=0
    i=0
    while (i<w):
        if(hist[i]>0):
            sample=np.array(head_sample[1][1])
            test=hist[i:i+len(sample)]
            if((sample==test).all()):  #模版匹配
                print("find :%s" % '流水号')
                i+=len(sample)
                continue
            if(not printflag):
                x_start=i
                printflag=True
            x_end=i
            print(hist[i],end=',')
        elif(printflag):
            printflag=False
            break
        i+=1
    
    #plt.plot(hist)
    plt.imshow(head[0:26,x_start:x_end])
    plt.show()


if __name__=="__main__":
    imgs=os.listdir("imgs")
    for imgname in imgs:
        imgdata=getimgdata(imgname) #将图片转换为白底黑字,去除掉图片杂质.
        data2img(imgdata,imgname)   #将图片数据存储到文件中
        cropimg(imgname)            #按行切割图片