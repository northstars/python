import pyaudio
import wave
import requests
import json
import base64
import os

from aip import AipSpeech

#百度语音识别APP ID
APP_ID = 'xx'

#百度语音识别APP KEY
API_KEY = 'xx'

#百度语音识别SECRET KEY
SECRET_KEY = 'xxx'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#获取声音文件
def GetSoundFile(FilePath):
	with open(FilePath,'rb') as fp:
		return fp.read()
		
#保存声音文件		
def SaveSound(text,FileName):
	result = client.synthesis(text,'zh',1,{'vol':5,'per':4})
	with open(FileName,'wb') as f:
		f.write(result)

#本地载入音频文件识别文字		
def LocalDiscernSound(FileName):
	SoundFile = GetSoundFile(FileName)
	result = client.asr(SoundFile,'pcm', 16000, { 'lan': 'zh',})
	return result["result"][0][:-1]

#获取Token
def GetToken():
    baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"
    url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(API_KEY, SECRET_KEY)
    res = requests.post(url)
    token = json.loads(res.text)["access_token"]
    return token

#提交音频数据到百度识别文字
def OnLineDiscernSound(fileurl,token):
    try:
        RATE = "16000"                  #采样率16KHz
        FORMAT = "wav"                  #wav格式
        CUID = "wate_play"
        DEV_PID = "1536"                #无标点普通话

        # 以字节格式读取文件之后进行编码
        with open(fileurl, "rb") as f:
            speech = base64.b64encode(f.read()).decode('utf8')

        size = os.path.getsize(fileurl)
        headers = {'Content-Type': 'application/json'}
        url = "https://vop.baidu.com/server_api"
        data = {
            "format": FORMAT,
            "rate": RATE,
            "dev_pid": DEV_PID,
            "speech": speech,
            "cuid": CUID,
            "len": size,
            "channel": 1,
            "token": token,
        }
        req = requests.post(url, json.dumps(data), headers)
        result = json.loads(req.text)
        return result["result"][0][:-1]
    except:
        return '识别不清'

'''
fileurl = 'e:/py/xiao/16k.wav'
token = GetToken()
text = OnLineDiscernSound(fileurl,token)
print(text)
FileName='e:/py/xiao/xuexi.wav'
text = '好好学习，天天向上'
SaveSound(text,FileName)
FileName='e:/py/xiao/16k.pcm'
text = LocalDiscernSound(FileName)
print(text)
'''