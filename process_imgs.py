from PIL import Image
import os


##切割图片
def cropimg(imgname):
    img=Image.open("imgs_processed/"+imgname)
    w,h=img.size
    img.crop((0, 0, w, 26*1)).save("crops/head_%s" % imgname)
    for i in range(1,11):
        if(h<26*(i+1)):break
        img.crop((0,26*i,w,26*(i+1))).save("crops/%d-%s" % (i,imgname))
    print('crop:',imgname,w,h)

##获取图片2值化数据
def process_img(imgname):
    if(os.path.isfile("imgs_processed/"+imgname)):
        return
    print('process:',imgname)
    srcimg=Image.open("imgs/"+imgname)
    size=srcimg.size
    dstimg=Image.new("RGBA",size)
    srcimg_p = srcimg.load()
    dstimg_p = dstimg.load()
    print(size)
    for x in range(size[0]):
        for y in range(size[1]):
            if(x<2 or y%26==0 or  y<2 or x>=size[0]-2 ): #左侧2列,上侧2行右侧2列设置为空白  ,每隔26行,这一行设置为空白
                dstimg_p[x,y]=(255,255,255,255)
            else:
                if(y<26):
                    if(srcimg_p[x,y][0]==0):  #如果是0表示黑色背景,转换为白色背景
                        dstimg_p[x,y]=(255,255,255,255)
                    else:
                        dstimg_p[x,y]=(0,0,0,255)
                else:
                    if(srcimg_p[x,y][0] in [192,255]):  #如果是这两种色,则设置为背景
                        dstimg_p[x,y]=(255,255,255,255)
                    else:
                        dstimg_p[x,y]=(0,0,0,255)
    dstimg.save("imgs_processed/"+imgname)



if __name__=="__main__":
    imgs=os.listdir("imgs")
    for imgname in imgs:
        process_img(imgname) #将图片转换为白底黑字,去除掉图片杂质.
        cropimg(imgname)            #按行切割图片