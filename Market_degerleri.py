# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 19:43:08 2021

@author: OSman VARIŞLI

her coinin marketlerini çekiyor.
"""
import requests
#from bs4 import BeautifulSoup
import pandas as pd 
from selenium import webdriver
import time


from selenium.webdriver.common.action_chains import ActionChains


def var_mi(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except:
        return False
    return True

def duzenle(arr):
    #print(arr)
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
        elif a==2:#Name
            try:
                me=metin.split('\n')
                v.append(me[0])
                v.append(me[1])
            except:
                v.append('Null')
                v.append('Null')
                
        elif a==3:#price
            v.append(metin.split('$')[1].replace(",", ""))
        elif a==4:#'24%'
            v.append(metin.split('%')[0])
        elif a==5:#'7%'
            v.append(metin.split('%')[0])
        elif a==6:#Market Cap
            v.append(metin.split('$')[1].replace(",", ""))
        elif a==7:#Volume(24h)
            metin=metin.split('\n')[0]
            v.append(metin.split('$')[1].replace(",", ""))
        elif a==8:#Circulating Supply
            v.append(metin.split(' ')[0].replace(",", ""))
        elif a==9:
            v.append(metin)
        elif a==10:
            v.append(metin)                                                             
        a=a+1 
    #print(v)
    return v


df_csv = pd.read_csv('sss.csv')

df = pd.DataFrame()
rows=[]
driver = webdriver.Firefox( executable_path='geckodriver.exe')
for index, row in df_csv.iterrows():
    print(index)
    """
    name=row['Name'].replace(' ','-').lower()
    name=name.replace('.','-').lower()
    
    driver.get('https://coinmarketcap.com/currencies/'+name+'/markets/')
    """
    try:#timeout
        driver.get(row['Link'])
    except:
        continue
    
    say=0
    yuklendimi=False
    while not yuklendimi:
        say=say+1
        print(say)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        s=0
        while True:
            s=s+1000
            driver.execute_script("window.scrollTo(0, "+str(s)+");")
            if s == 9000:
                break
            
        if var_mi("//button[@class='x0o17e-0 DChGS sc-10p9viq-6 gMdA-DH']/a"):
            try:
                element=driver.find_element_by_xpath("//button[@class='x0o17e-0 DChGS sc-10p9viq-6 gMdA-DH']/a")
                ActionChains(driver).move_to_element(element).click().perform()
                time.sleep(1)    
            except:
                print('Hata oldu....')
        else:
            print('yokkk')
        

        r = driver.find_elements_by_xpath ("//table[@class= 'h7vnx2-2 ecUULi cmc-table  ']/tbody/tr")
        c = driver.find_elements_by_xpath ("//*[@class= 'h7vnx2-2 ecUULi cmc-table  ']/tbody/tr[3]/td")
        rc = len (r)
        cc = 2#len (c)
        for i in range (1, rc + 1) :
            v=[]
            v.append(row['Name'])
            for j in range (1, cc + 1) :
                try:d = driver.find_element_by_xpath ("//tr["+str(i)+"]/td["+str(j)+"]").text
                except: d='ssss'
                v.append(d)
                
            try:
                v=duzenle(v)
            except:
                print(v)
                
            try:
                Total_Supply=driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[4]/div[4]/div[2]").text.replace(",", "")
            except:
                Total_Supply=driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div/div[1]/div[3]/div/div[3]/div[1]/div[4]/div[4]/div[2]").text.replace(",", "")

                                           
            v.append(Total_Supply)
            
            print(v)
            if d=='ssss': yuklendimi=False
            else: 
                yuklendimi=True
                rows.append(v)
        if say==20: 
            yuklendimi=True
                #10 kere dene sayfa yükelenmediyse artık yapaak bi şey yok.
    #print(rows)


df=df.append(rows)

df.columns = ['Coin','No', 'Market', 'Z1', 'Z2','Total_Supply']
df=df.drop(['No','Z1','Z2'], axis=1)
#print(df)
#df=df.groupby("Coin")["Market"].count()
#print(df)
    
df.to_csv('Market_degerleri.csv')
driver.close()              
              
              
              