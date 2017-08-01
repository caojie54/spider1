#!usr/bin/env python3
# _*_ coding: utf-8 _*_ 
''' i want get many pictures on taobao website	'''
import requests
import re
main_url = 'https://www.hao123.com/'
scraped_url = [];
current_page_url= []
def scrape(url):
    if existed(url) == True:
        print("this page is over")
    else:
        try:    
            r = requests.get(url)
            get_need_data(r.text)
            #print(r.text)
            #add url into scraped_url,
            scraped_url.append(url)
            with open("/home/caojie/url.txt",'a') as f:
                f.write(url)
            for url in re.findall("<a href=(.*?)>",r.text,re.S):
                print(url)
                scrape(url)
        except Exception as e:
            print("Exception occur %s" % e)

#existed in scraped_url,already been scraped
def existed(url):
    if url in scraped_url:
	    return True
    return False

def get_need_data(url):
    pass

if __name__=='__main__':
    print('hello,world!')
    print(main_url)
    scrape(main_url)
   




         
                    



                        






