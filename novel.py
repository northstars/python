import chardet
import requests
from lxml import etree
import time
from baidu import BaiDuYuYin

class Novel:
	def __init__(self):
		self.session = requests.session()
		self.session.headers["user-agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
	
	#获取章节	
	def GetChapters(self, url):
		r = self.session.get(url)
		r.encoding = chardet.detect(r.content).get("encoding", "utf-8")
		html = etree.HTML(r.text)
		for item in html.xpath("//dl/dd/a"):
			yield item.attrib["title"], url + item.attrib["href"]
	
	#保存文件		
	def SaveFile(self,filename,str):
		with open(filename,'a',encoding='utf-8') as f:
			f.write(str)
	#保存音频		
	def SaveMp3(self,filename,str):
		with open(filepath+'.mp3', "ab") as fp:
			fp.write(str)
	
	#获取内容		
	def GetContent(self, url, title):
		r = self.session.get(url)
		yuyin = BaiDuYuYin()
		
		r.encoding = chardet.detect(r.content).get("encoding", "utf-8")
		html = etree.HTML(r.text)
		name = html.xpath("//div[@id='info']")
		for info in html.xpath("//div[@id='content']"):
			text = info.xpath("string(.)")
			lstr = title
			for line in text.split("。"):
				lstr += line +'\n'
				content = yuyin.SaveSound(title,line)
			return lstr	
			
	#获取小说		
	def GetNovel(self):
		weburl = "http://www.biquge.info/61_61256/"
		num = 1
		filename = 'novel.txt'
		for title, url in self.GetChapters(weburl):
			if num < 10 :
				#print(title, url)
				text = self.GetContent(url,title)
				self.SaveFile(filename,text)
				num += 1
				time.sleep(2)
		
		

nove = Novel()
nove.GetNovel()





















