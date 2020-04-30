#!/usr/bin/env python
# coding: utf-8

# In[130]:


from datetime import datetime #класс datetime из модуля datetime

format = '%Y.%m.%d.%H.%M.%S'
ext='.csv'

number=1
while number<=27:
    if (number!=12) and (number!=20):
        url1='https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID='
        url2='&year1=1981&year2=2020&type=Mean'
        url3='%s%s%s' %(url1, number, url2) #маска
        import urllib.request #модуль для открытия ссылок
        vhi_url = urllib.request.urlopen(url3)
        path = r'D:\anaconda\lab 1\vhi_id_16_2'
        new_path = '%s_%s_%s%s' % (path, number, datetime.now().strftime(format), ext)
        with open(new_path,'wb') as out: #открываем файл для записи и называем out
            out.write(vhi_url.read()) #записываем в файл то что считано со ссылки
            out.close()
        print ("VHI is downloaded...")
        number+=1
    else:
        number+=1
print ("download finished...")


# In[131]:


from pathlib import Path #из модуля pathlib (работа с путями файлов) класс Path
import os #модуль для работы с ос

path = Path(r'D:\anaconda\lab 1')
mask = '*.csv'
    
for files in path.glob(mask): #находит все файлы соответствующие маски по данному пути
    x = files.name.split("_")
    dict = {'1': '22', '2':'24', '3':'23', '4':'25', '5':'03', '6':'04', '7':'08', '8':'19', '9':'20', '10':'21', 
            '11':'09', '13':'10', '14':'11', '15':'12', '16':'13', '17':'14', '18':'15', '19':'16', '21':'17', 
            '22':'18', '23':'06', '24':'01', '25':'02', '26':'07', '27':'05'}
    #print(x)
    x[4]=dict.get(x[4])
    new ='_'.join(x)
    t = files.name
    #print(t)
    directory = r'D:\anaconda\lab 1\\'
    
    old_file = os.path.join(directory, t)
    new_file = os.path.join(directory, new)
    os.rename(old_file, new_file)
    
print('done')


# In[163]:


import pandas as pd #модуль для работы с датафреймами
from pathlib import Path
import os
import glob #оперирует путями файлов

dict = {'01':'Вінницька область', '02':'Волинська область', '03':'Дніпропетровська область', '04':'Донецька область', 
        '05':'Житомирська область', '06':'Закарпатська область', '07':'Запорізька область', '08':'Івано-Франківська область', 
        '09':'Київська область', '10':'Кіровоградська область', '11':'Луганська область', '12':'Львівська область', 
        '13':'Миколаївська область', '14':'Одеська область', '15':'Полтавська область', '16':'Рівенська область', 
        '17':'Сумська область', '18':'Тернопільська область', '19':'Харківська область', '20': 'Херсонська область', 
        '21':'Хмельницька область', '22':'Черкаська область', '23':'Чернівецька область', '24':'Чернігівська область', 
        '25':'Республіка Крим'}

mask = '*.csv'
path = Path(r'D:\anaconda\lab 1')

def readFile(path):
    df = pd.read_csv(path, sep = ',', index_col=7)
    df.columns = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'index8', 'index9'] 
    p=str(path) #превращаем путь в строчку чтоб дальше с ним работать
    index = p.split("_")[4]
    df['Region'] = dict.get(index)
    del df['index8']
    del df['index9']
    return df

mydir = os.path.abspath(os.curdir) #находит абсолютный (полный?) путь для директории где мы сейчас находимся
df = pd.concat([readFile(file) for file in path.glob(mask)], ignore_index=True) #ignore_index игнорирует колонку индексов в каждом фрейме
df = df[(df.VHI != -1)]
df.drop(df.tail(1).index,inplace=True)
df.drop(df.index[[]])


# In[118]:


#по областям и годам + экстремумы

def filters(df): 
    df_filtered = df.loc[(df['Year']== '2020') & (df['Region'] == 'Київська область')]
    return df_filtered

print(filters(df))
print("max:",filters(df)['VHI'].max())
print("min:",filters(df)['VHI'].min())


# In[145]:


#посухи

def filters(df): 
    df_filtered = df.loc[(df['Region'] == 'Київська область')& (df['VHI'] < 15)] #ектремальна df.loc - метки
    #df_filtered = df.loc[(df['Region'] == 'Київська область')& (df['VHI'] > 15) & (df['VHI'] < 35)] #помірна 
    df.drop(df.tail(1).index,inplace=True)
    return df_filtered

print(filters(df))
