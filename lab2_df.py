import os
import glob
import pandas as pd
import urllib.request
from pathlib import Path
from datetime import datetime
import pickle

url1 = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID='
url2 = '&year1=1981&year2=2020&type=Mean'
path = r'D:\lab_data_science\vhi_id_16_'
path1 = Path(r'D:\lab_data_science\\')
mask = '*.csv'
FORMAT = '%Y.%m.%d.%H.%M.%S'
ext = '.csv'
dict_province = {1: '22', 2:'24', 3:'23', 4:'25', 5:'03', 6:'04', 7:'08', 8:'19', 9:'20', 10:'21',
            11:'09', 13:'10', 14:'11', 15:'12', 16:'13', 17:'14', 18:'15', 19:'16', 21:'17',
            22:'18', 23:'06', 24:'01', 25:'02', 26:'07', 27:'05'}
dict_names = {
    '01':'Вінницька область', '02':'Волинська область', '03':'Дніпропетровська область',
    '04':'Донецька область', '05':'Житомирська область', '06':'Закарпатська область',
    '07':'Запорізька область', '08':'Івано-Франківська область', '09':'Київська область',
    '10':'Кіровоградська область', '11':'Луганська область', '12':'Львівська область',
    '13':'Миколаївська область', '14':'Одеська область', '15':'Полтавська область',
    '16':'Рівенська область', '17':'Сумська область', '18':'Тернопільська область',
    '19':'Харківська область', '20': 'Херсонська область', '21':'Хмельницька область',
    '22':'Черкаська область', '23':'Чернівецька область', '24':'Чернігівська область',
    '25':'Республіка Крим'}


def DownloadFiles():
    if len(os.listdir(r'D:\lab_data_science\\')) == 0:
        print("download started.")
        for province in dict_province.keys():
            url3 = f'{url1}{province}{url2}'
            vhi_url = urllib.request.urlopen(url3)  # открываем ссылку
            new_name = dict_province[province]
            new_path = f'{path}_{new_name}_{datetime.now().strftime(FORMAT)}{ext}'
            with open(new_path, 'wb') as out:  # открываем файл для записи
                out.write(vhi_url.read())  # записываем в файл то что считали с открытой ссылки
            print(f"VHI {province} is downloaded.")
        print("download finished.")
    else: print("аiles already downloaded.")

def Readfile(pat):
    df = pd.read_csv(pat, sep = ',' )
    df.columns = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'index8', 'index9', 'index10']
    p=str(pat)
    index = p.split("_")[6]
    df['Region'] = dict_names.get(index)
    df = df[['Year', 'Week', 'Region', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']]
    return df

def BuildDF():
    print("build started")
    df = pd.concat([Readfile(file) for file in path1.glob(mask)], ignore_index=True)  # собирает фреймы вместе, не учитывая колонку индексов каждого из них
    df = df.loc[(df['VHI'] != -1) & (df.Year != '</pre></tt>')]  # убираем лишние строчки
    df.drop(df.index[[]])
    print("build finished")
    return df


DownloadFiles()
df_1 = BuildDF()

print(df_1)

with open('pickledata.p', 'wb') as file:
    pickle.dump(df_1, file)
