#!/usr/bin/env python
#coding=utf-8
#Author:Richard Liu
#Blog: http://richardxxx0x.wicp.net
#Email:<richardxxx0x@gmail.com>

"""
.------..------..------..------..------..------..------.
|D.--. ||O.--. ||M.--. ||A.--. ||I.--. ||N.--. ||S.--. |
| :/\: || :/\: || (\/) || (\/) || (\/) || :(): || :/\: |
| (__) || :\/: || :\/: || :\/: || :\/: || ()() || :\/: |
| '--'D|| '--'O|| '--'M|| '--'A|| '--'I|| '--'N|| '--'S|
`------'`------'`------'`------'`------'`------'`------'
get ip/domain the same domains 

USAGE: python getdomains.py  <domains/ip>
EXAMPLE: python getdomains.py 5.yao.cl
         python getdomains.py 184.154.128.246
"""

import sys
import socket
import requests
import threading
import Queue
import time


##ctrl+c to exit.
sys.tracebacklimit = 0
queue = Queue.Queue()
class GetDomain():
  def __init__(self):
    pass
  
  def get_domains(self,ip):
    print "正在获取域名，请稍后......"
    print "按 ctrl+c 退出程序"
    domains = []
    try:
      url = "http://dns.aizhan.com/index.php?r=index/domains&ip=%s&page=1" % (ip)
      r = requests.get(url,timeout = 5)
      r.close()
      domains = (r.json()["domains"])
      maxpage = r.json()["maxpage"]
      if maxpage >= 2:
          for i in range(2,maxpage+1):
            url = "http://dns.aizhan.com/index.php?r=index/domains&ip=%s&page=%d" % (ip,i)
            r = requests.get(url,timeout = 5)
            r.close()
            domains = domains+r.json()["domains"]
      self.domains = domains
      return domains
    except Exception:
      exit(0)
  
  
def get_title(domain):
    url = "http://dns.aizhan.com/index.php?r=index/title&url=%s" % (domain)
    try:
      r = requests.get(url,timeout = 5)
      r.close()
      str = domain+"   =====> "+ r.text
      print str
    except Exception:
      pass
  
    
class GetTitleThread(threading.Thread):
  def __init__(self,queue):
    threading.Thread.__init__(self)
    self.queue = queue
  def run(self):
    while True:   
      domain = self.queue.get()
      get_title(domain)
      self.queue.task_done()


def main():
  start = time.time()
  ip = sys.argv[1]
  if ip.replace('.','').isdigit():
    ip = ip
  else:
    ip = socket.gethostbyname(ip)
  
  gd = GetDomain()
  domains = gd.get_domains(ip)
  num = len(domains)
  
  for i in range(5):
    t = GetTitleThread(queue)
    t.setDaemon(True)
    t.start()
    
  for i in range(0,num):
    domain = domains[i]
    queue.put(domain)
    
  queue.join()
   
  print "Elapsed Time: %s\n" % (time.time() - start)
  print '如果显示 "页面获取失败" ，说明这个网址可能需要翻墙才可以访问!'
  

if __name__ == "__main__":
  print __doc__
  if len(sys.argv) == 2:
    main()
