import pyaudio
import wave
import requests
import json
import base64
import os

from aip import AipSpeech

class BaiDuYuYin:
	def __init__(self):
		self.APP_ID = '16416498'
		self.API_KEY = 'xx'
		self.SECRET_KEY = 'xx'
		self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
		
	#获取声音文件
	def GetSoundFile(self,FilePath):
		with open(FilePath,'rb') as fp:
			return fp.read()
		
	#保存声音文件		
	def SaveSound(self,FileName,text):
		result = self.client.synthesis(text,'zh',1,{'vol':5,'per':4})
		with open(FileName+'.mp3','ab') as f:
			f.write(result)

	#本地载入音频文件识别文字		
	def LocalDiscernSound(self,FileName):
		SoundFile = self.GetSoundFile(FileName)
		result = self.client.asr(SoundFile,'pcm', 16000, { 'lan': 'zh',})
		return result["result"][0][:-1]

	#获取Token
	def GetToken(self):
	    baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
	    grant_type = "client_credentials"
	    
	    url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(self.API_KEY, self.SECRET_KEY)
	    res = requests.post(url)
	    token = json.loads(res.text)["access_token"]
	    return token
	    #print(token)

	#提交音频数据到百度识别文字
	def OnLineDiscernSound(self,fileurl,token):
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
if __name__ == '__main__':
	YuYin = BaiDuYuYin()
	
	fileurl = '16k.wav'
	token = YuYin.GetToken()
	text = YuYin.OnLineDiscernSound(fileurl,token)
	print(text)
	FileName='xuexi'
	text = '好好学习，天天向上'
	YuYin.SaveSound(FileName,text)

	FileName='16k.pcm'
	text = YuYin.LocalDiscernSound(FileName)
	print(text)
'''