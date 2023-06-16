# -*- encoding: utf-8 -*-
#
#Time    :   2023/05/11 10:25:59
#Author  :   zbchu
# ==============================================================================
"""利用chatgpt提取评论主题"""

import pandas as pd
import requests
from time import sleep
from tqdm import tqdm
import json
import sys
from concurrent.futures import ThreadPoolExecutor

file_name = sys.argv[1]

def extract_topic(msg):
    headers = {'Content-type': 'application/json'}
    data = {'msg': msg}
    data = json.dumps(data, ensure_ascii=False).encode('utf-8')

    link = 'http://your_ip:port/topic'

    try:
        response = requests.post(link,
                                 data=data,
                                 headers=headers).json()
        if response['code'] == 200:
            return response['resmsg']['choices'][0]['message']['content']
        else:
            print(response)
    except:
        raise

def add_topic(df, ind, step):
    for i in tqdm(range(ind, ind+step)):
        if df.loc[i, 'comment'] != '':
            try:
                df.loc[i, 'topic'] = extract_topic(df.loc[i, 'comment'])
                sleep(0.5)
            except KeyboardInterrupt:
                break
                print("Interrupted by user.")

df = pd.read_csv(file_name)
df['comment'] = df.comment.fillna('')
df['topic'] = ''

lens = len(df)
step = lens // 10

with ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(0, lens, step):
        executor.submit(add_topic, df, i, step)

df.to_csv(file_name+'_result.csv')
