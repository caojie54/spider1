# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 09:51:09 2017

@author: caojie
"""
import requests,random
from lxml import etree
#get https proxy from https://www.sslproxies.org/
def get_proxy():
    r = requests.get("https://www.sslproxies.org/")
    tree = etree.HTML(r.content)
    ip = tree.xpath("//table[@id='proxylisttable']/tbody/tr/td[1]/text()")
    port = tree.xpath("//table[@id='proxylisttable']/tbody/tr/td[2]/text()")
    urls=[]
    for i in range(len(ip)):
        url=ip[i]+":"+port[i]
        #print(url)
        urls.append(url)
    return urls

class ProxyPool(object):
    '''A proxypool class to obtain proxy'''
    def __init__(self):
        self.pool = set()
        
    def updateGatherProxy(self):
        '''Use GatherProxy to update proxy pool '''
        self.pool.update(get_proxy())
        
    def removeproxy(self,proxy):
        '''remove a proxy from pool'''
        if (proxy in self.pool):
            self.pool.remove(proxy)
    
    def randomchoose(self):
        '''Random Get a proxy from pool'''
        if (self.pool):
            return random.sample(self.pool,1)[0]
        else:
            self.updateGatherProxy()
            return random.sample(self.pool,1)[0]
    def getproxy(self):
        '''get a dict format proxy randomly'''
        proxy=self.randomchoose()
        proxies={'http':'http://'+proxy,'https':'http://'+proxy}
        print("test:"+str(proxies)+"by request https://aso100.com/")
        #proxies={'https':'http://'+proxy}
        try:
            #r=requests.get('http://dx.doi.org',proxies=proxies1,timeout=3)
            r=requests.get('https://aso100.com/',proxies=proxies,timeout=5)
            if (r.status_code == 200):
                print("get new useful proxies"+str(proxies))
                return proxies
            else:
                self.removeproxy(proxy)
                return self.getproxy()
        except:
            self.removeproxy(proxy)
            return self.getproxy()
    
if __name__ == '__main__':
    proxypool = ProxyPool()
    print("get proxy:"+str(proxypool.getproxy()))
       