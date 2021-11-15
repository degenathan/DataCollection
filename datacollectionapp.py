
"""
Please run this section of code if missing a python library
import sys
!{sys.executable} -m pip install sodapy

import sys
!{sys.executable} -m pip install pandas

"""


#API Key ID
#9yz7a9cjftdr9qbvdlhz4ii9l

#API Key Secret
#e48r6otlbnf9bt6qd6ymci5hudrbwbk582ulbccarit04orlr



from sodapy import Socrata
from sys import exit
import pandas as pd
import numpy as np
import urllib3
import json


def search(a,b,c):
    
    print("Input fields or NA")
    print("If searching a state government type state name in city and state feilds")
    city = a
    state = b
    category_name = c
    
    city_api_list = pd.read_csv("city_api_list.csv", index_col = False)
        
    #if city_api_list.loc[city_api_list['City'].str.contains(city)] != None:
    if city_api_list["City"].eq(city).any() and city_api_list["State-Abbr."].eq(state).any():
        #print('True')
        x = city_api_list.loc[city_api_list['City'].str.contains(city)]
        x = x.loc[x['State-Abbr.'].str.contains(state)]['API-site']
        x = str(x).split()
        x = x[1]
        var = '?search_context=' + str(x)
        var = var + '&q=' + str(category_name)
        return var
    
    else:
        print("City Not Found.")


def mainprogram():
    
    
    stoprg = 0
    
    while stoprg == 0:
        city_domain = str(search())
    
        http = urllib3.PoolManager()
    
        #?domains=data.austintexas.gov'
    
        request_site = 'https://api.us.socrata.com/api/catalog/v1'+ city_domain
        print(request_site)
        
        request = http.request('GET',request_site)
    
        #response_body = urlopen(request).read()
        data = json.loads(request.data)
        #print(data)
        while True: 
            try:
                results_df = pd.json_normalize(data['results'])
                break
            except KeyError:
                print("No result found.")
                print()
                main()
                
        #DataFrame.from_records(str(request.data))
        
        results_df['Index'] = range(1,len(results_df)+1)
        #print(results_df)
        results_df.set_index('Index')
        #['resource.name']
        a = pd.DataFrame(data, columns = ['Index', 'Name'], index = None)
        a['Index'] = results_df['Index']
        a['Name'] = results_df['resource.name']
        print(results_df[['Index','resource.name']].to_string(index=False))
        #results_df.to_csv('results_test.csv')
        print()
        print("Select datasets seperated by commas", end = "")
        num_select = input("or type NA for none: ")
        if num_select != 'NA':
            num_select = num_select.split(",")
            for i in num_select:
                i = int(i)-1  
                #results_df.loc[i]
                x = results_df.iloc[i]
                z = x['resource.id']
                y = x['metadata.domain']
                #print(z)
                client = Socrata(y, None)
                results = client.get(z)
                final = pd.DataFrame.from_records(results)
                
                #data = json.loads(request.data)
                #final = pd.json_normalize(data['results'])
                
                y = results_df.loc[i]['resource.name'] + '.csv'
                final.to_csv(y)
                print("Downloaded", y)  

        ystop = input("Continue with another city/topic? (y/n): ")
        if ystop == 'n':
            stoprg += 1
            exit()
        
        
          
    #print(request.data)
    
    '''
    
    client = Socrata("https://api.us.socrata.com/api/catalog/v1/domains", None)
    results = client.get()
    results_df = pd.DataFrame.from_records(results)
    
    topic = input("Topic of interest: ")
    print(topic)
    '''


