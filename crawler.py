#!usr/bin/env python3
# _*_ coding: utf-8 _*_ 
''' i want get many pictures on taobao website	'''
import requests
import re
main_url = 'http://www.taobao.com'
scraped_url = [];
current_page_url= []
def scrape(url):
    print(existed(url))
    if existed(url) == True:
        print("1")
        pass
    else:
        print("2")
        r = requests.get(url)
        get_need_data(r.text)
        #print(r.text)
        #add url into scraped_url,
        scraped_url.append(url)
        for url in re.findall("<a href=.*?>",r.text,re.S):
            print(url)

#existed in scraped_url,already been scraped
def existed(url):
    print(scraped_url)
    if url in scraped_url:
	    return True
    return False

def get_need_data(url):
    pass

if __name__=='__main__':
    print('hello,world!')
    print(main_url)
    scrape(main_url)
   




         
                    



                        






