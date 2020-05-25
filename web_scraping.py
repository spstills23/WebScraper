# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:48:31 2020

@author: seans
"""

# Import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from re import findall

#Get URL and extract content
url = requests.get('https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/')
c = url.content

# Create a soup object
soup = BeautifulSoup(c, 'html.parser')

#inspect the webpage and find where the info you want is
my_table = soup.find('table', attrs = {'class': 'contenttable'}) #ex (<table>, class was 'contenttable')

#the data is between the <tr> tags so grab it using the find_all function
data=[]
for link in my_table.find_all('tr'):
    data.append(link.get_text())
data

#then you clean up and slice out the data you dont need
del data[0:2]
del data[18:21]
data
#use regex to find the values we ultimatly want from the data list (province:cases)
real_data=[]
for i in range(0,18):
    pattern = re.compile('[0-9][0-9] - (.*)')
    result = pattern.findall(data[i])
    real_data.append(result)
real_data

#Creating the separate lists to split the strings
regions=[]
cases=[]
for i in range(0,18):
    strings = ''.join([i for i in real_data[i] if not i.isdigit()])
    no_numbers = ''.join([i for i in strings if not i.isdigit()])
    no_letters = ''.join(filter(lambda x: x.isdigit(), strings))
    regions.append(no_numbers)
    cases.append(no_letters)
    
regions
cases

#Now we can enter them into a df to use for later modeling
#Dataframe
df=pd.DataFrame()
df['regions'] = regions
df['cases'] = cases
df.head()