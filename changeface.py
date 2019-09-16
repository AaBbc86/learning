'''用Face++的API,登录https://console.faceplusplus.com.cn/login去注册，然后新建应用，需要API Key和API Secret
'''
import json
import requests
import simplejson
import base64

#加载图片
image1=r'/myproject/tmp/1.jpg'
image2=r'/myproject/tmp/2.jpg'
image=r'/myproject/tmp/result.jpeg'

#第一步获取人脸的关键点,脸的上下左右四个点边缘确定一个矩形
def find_face(imgpath):
    print('finding')
    #直接调用api,获取人脸
    http_url='https://api-cn.faceplusplus.com/facepp/v3/detect'
    #请求api时需要携带的数据
    data={"api_key":'-GtQh3abD-3XW-5pUjM8vZTVgccD02Ij',
          "api_secret":'49FasvxEj1TSgCDe-IR-hZz5SwTM1TPb',
          "image_url":imgpath,
          "return_landmark":1
            
   }
    files={"image_file":open(imgpath,'rb')}
    #因为要携带数据，所以下面是post请求
    response=requests.post(http_url,data=data,files=files)
    req_con=response.content.decode('utf-8')
    this_json=simplejson.loads(req_con)
    faces=this_json['faces']
    list0=faces[0]
    rectangle=list0['face_rectangle']
    return rectangle

#第二步换脸（注意图片大小不要超过2M）
def merge_face(image_url1,image_url2,image_url,number): #number的作用是决定换脸的相似度
    ff1=find_face(image_url1)
    ff2=find_face(image_url2)
    rectangle1=str(str(ff1['top'])+","+str(ff1['left'])+","+str(ff1['width'])+","+str(ff1['height']))
    rectangle2=str(str(ff2['top'])+","+str(ff2['left'])+","+str(ff2['width'])+","+str(ff2['height']))
    f1=open(image_url1,'rb')
    f1_64=base64.b64encode(f1.read())
    f1.close()
    f2=open(image_url2,'rb')
    f2_64=base64.b64encode(f2.read())
    f2.close()

    #调用api进行合并人脸
    url_add='https://api-cn.faceplusplus.com/imagepp/v1/mergeface'
    data={"api_key":'-GtQh3abD-3XW-5pUjM8vZTVgccD02Ij',
          "api_secret":'49FasvxEj1TSgCDe-IR-hZz5SwTM1TPb',
          "template_base64":f1_64,  
          "template_rectangle":rectangle1,
          "merge_base64":f2_64,
          "merge_rectangle":rectangle2,
          "merge_rate":number
            }
    response1=requests.post(url_add,data=data)
    req_con1=response1.content.decode('utf-8')
    req_dict=json.JSONDecoder().decode(req_con1)
    result=req_dict['result']
    imgdata=base64.b64decode(result)
    file=open(image_url,'wb')
    file.write(imgdata)
    file.close()
#将图片2的脸换到1上面
merge_face(image1,image2,image,100)
