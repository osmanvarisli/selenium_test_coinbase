# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 14:50:23 2021

@author: Osman VARIŞLI
oldu bu oldu
"""

import requests
#from bs4 import BeautifulSoup
import pandas as pd 
from selenium import webdriver
import time

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
def var_mi(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except:
        return False
    return True

def duzenle(arr):
    print(arr)
    a=0
    v=[] 
    for td in arr:
        ham_metin=td
        metin=td
        if metin=='--':
           v.append(0) 
        elif a==0:
            v.append(metin)
        elif a==1:#No
            v.append(metin)
        elif a==2:#No
            v.append(metin)
        elif a==3:#Name
            try:
                me=metin.split('\n')
                v.append(me[0])
                v.append(me[1])
            except:
                v.append('Null')
                v.append('Null')
                
        elif a==4:#price
            if metin in '...':
                v.append('0')
            else:
                v.append(metin.split('$')[1].replace(",", ""))
        elif a==5:#'24%'
            v.append(metin.split('%')[0])
        elif a==6:#'7%'
            v.append(metin.split('%')[0])
        elif a==7:#Market Cap
            v.append(metin.split('$')[1].replace(",", ""))
        elif a==8:#Volume(24h)
            metin=metin.split('\n')[0]
            v.append(metin.split('$')[1].replace(",", ""))
        elif a==9:#Circulating Supply
            v.append(metin.split(' ')[0].replace(",", ""))
        elif a==10:
            v.append(metin)
        elif a==11:
            v.append(metin)                                                             
        a=a+1 
    #print(v)
    return v
df = pd.DataFrame()
rows=[]
driver = webdriver.Firefox( executable_path='geckodriver.exe')
for i in range(1,16):
    driver.get('https://coinmarketcap.com/?page='+str(i))

    s=0
    while True:
        s=s+1000
        driver.execute_script("window.scrollTo(0, "+str(s)+");")
        if s == 9000:
            break
          
    #htmltable = driver.find_element_by_class_name('cmc-table')
       
    r = driver.find_elements_by_xpath ("//table[@class= 'h7vnx2-2 czTsgW cmc-table  ']/tbody/tr")
    c = driver.find_elements_by_xpath ("//*[@class= 'h7vnx2-2 czTsgW cmc-table  ']/tbody/tr[3]/td")
    rc = len (r)
    cc = len (c)
    for i in range (1, rc + 1) :
        v=[]
        for j in range (1, cc + 1) :
            try:
                d = driver.find_element_by_xpath ("//tr["+str(i)+"]/td["+str(j)+"]").text
            except:
                d='ssss'
            
            if j== 3:
                if var_mi("//tr["+str(i)+"]/td["+str(j)+"]/div/a[@class='cmc-link']"):
                    a=driver.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]/div/a[@class='cmc-link']").get_attribute('href')    
                    a=a+'markets/'
                else:
                    a='yok'
                v.append(a)
            if var_mi("//tr["+str(i)+"]/td["+str(j)+"]/span/span[@class='icon-Caret-down']"):
                p_n='-'
            else:
                p_n=''
            v.append(p_n+d)
        try:
            v=duzenle(v)
        except:
            print(v)
        
        #d=driver.find_element_by_xpath("//div/div/div[1]/div[2]/div/div[2]/div/span/a[2]").get_attribute('href')
        #print('https://coinmarketcap.com/'+d)
        #v.append('https://coinmarketcap.com/'+d)

        rows.append(v)
driver.close()


#df.columns = ['No', 'Name', 'Price', '24h', '7d', ' Market Cap  Volume(24h)', 'Circulating Supply', 'Z1']  	
#df=df.set_index('1')
df=df.append(rows)
print(df)
df.columns = ['s','No','Link','Name','Symbol', 'Price', '24h', '7d', ' Market Cap ',' Volume 24h', 'Circulating Supply', 'Z1', 'Z2']
df=df.set_index('No')
df=df.drop(['s', 'Z1', 'Z2'], axis=1)
#df['oran']=df['Price']/df['Circulating Supply']
#df=df.sort_values(by=['oran'])
print(df)
    
df.to_csv('sss.csv')

    
    
