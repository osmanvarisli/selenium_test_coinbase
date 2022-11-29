# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 11:22:36 2021

@author: PC
"""
import requests
import pandas as pd 
from selenium import webdriver
import time

def sorgula(market_df,ddff,olmamali=[],olmali_x=[]):
    """
    print('osman')
    d_m_olmali=market_df[market_df.Market == olmali_x]
    print(d_m_olmali)
    print('osman')
    print('osman')
    print('osman')
    print('osman')
    """
    d_m=market_df[market_df.Market == olmamali]
    print(d_m)
    d_m=d_m.drop(['Market'], axis=1)
    return_df=ddff
    return_df=return_df.reset_index()
    for index,row in d_m.iterrows():
        return_df=return_df[return_df.Coin != row['Coin']]
    return return_df
    
    """
    for index, row in ddff['coin'].iterrows(): 
        if row not in d_m:
    """        
                
df= pd.read_csv('Market_degerleri.csv')
df=df.set_index('Unnamed: 0')
df3=df.groupby(['Coin','Total_Supply']).count()
df3=df3.sort_values(by='Market', ascending=False)

print(df3.sort_values(by='Total_Supply', ascending=True))

df2= pd.read_csv('sss.csv')



df2=df2.set_index('No')
df2['Price'] = df2['Price'].astype(float)
#df2=df2[df2['Price']<1]
df2=df2[df2['Circulating Supply']<50000000]
#df2=df2[df2['Price']>0.005]
df2['s']=df2['Price']*df2['Circulating Supply']
df2=df2.sort_values(by='s', ascending=False)



ddff=df3.join(df2.set_index('Name'), on='Coin')
ddff=ddff[ddff.Market>20]
ddff=ddff[ddff.Price<15]
ddff=ddff[ddff.Price>0.005]
#ddff=ddff[ddff['Circulating Supply']<50000000]
ddff=ddff.sort_values(by='s', ascending=True)
print(ddff.columns)
olmamali='Binance'#market isimleri
olmamali=''
olmali_x='Binance'

ddff=sorgula(df,ddff,olmamali,olmali_x)


#print(ddff.head(30))
print(ddff[['Symbol','Market', 'Price', 'Circulating Supply', 's']].head(50))
