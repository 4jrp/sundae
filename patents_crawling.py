# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 16:24:43 2017

@author: JongRyul
"""

import urllib
# print(urllib.parse.unquote("%64%6F%72%69%72%69")) # doriri
# print(urllib.parse.quote('자동차 샤시')) # %EC%9E%90%EB%8F%99%EC%B0%A8%20%EC%83%A4%EC%8B%9C
# print(urllib.parse.quote('q=자동차+샤시&num=100')) # q%3D%EC%9E%90%EB%8F%99%EC%B0%A8%2B%EC%83%A4%EC%8B%9C%26num%3D100

site_url='https://patents.google.com/xhr/query?url=q%3D'
query='자동차+샤시'; query_url=urllib.parse.quote(query)
page_filter=urllib.parse.quote('&page=') # page를 나타내주는 변수 필요. 0부터 시작.
page=str(0)
num_filter=urllib.parse.quote('&num=100')
rear_url='&exp='



import requests
# 'url' corresponing to the query.
url = site_url+query_url+page_filter+page+num_filter+rear_url
# https://patents.google.com/xhr/query?url=q%3D%EC%9E%90%EB%8F%99%EC%B0%A8%2B%EC%83%A4%EC%8B%9C%26page%3D0%26num%3D100&exp=
# 'r' received data corresponding to url from Server.
r = requests.get(url)
print(r)
results=r.json()['results']
print("total_num_results:\t", results['total_num_results'])
print("total_num_pages:\t", results['total_num_pages'])
totN_page = results['total_num_pages']

p_number=[]
filing_date=[]
priority_date=[]
assignee=[]
title=[]
snippet=[]
for page_idx in range(totN_page):
    print('page_idx=',page_idx)
    page=str(page_idx)
    url=site_url+query_url+page_filter+page+num_filter+rear_url
    r=requests.get(url)
    results=r.json()['results']
    results_cl=results['cluster']
    result=results['cluster'][0]['result']
    if len(result) < 1:
        continue
    for p_idx in range(len(result)):
        p_number.append(result[p_idx]['patent']['publication_number'])
        filing_date.append(result[p_idx]['patent']['filing_date'])
        priority_date.append(result[p_idx]['patent']['priority_date'])
        assignee.append(result[p_idx]['patent']['assignee'])
        title.append(result[p_idx]['patent']['title'])
        snippet.append(result[p_idx]['patent']['snippet'])



import pandas as pd
# Create a Pandas dataframe from the data.
patents_df=pd.DataFrame({'p_number':p_number, 'filing_date':filing_date, 'priority_date':priority_date,
                 'assignee':assignee, 'title':title, 'snippet':snippet})
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer=pd.ExcelWriter('patents_df.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
patents_df.to_excel(writer, sheet_name=query)
# Close the Pandas Excel writer and output the Excel file.
writer.save()









