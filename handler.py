import numpy as np
import pandas as pd
# import zipfile
import pandas as pd
# from io import BytesIO
def process_data():
    # with zipfile.ZipFile('dataset.zip', 'r') as zipf:
    #     file_list = zipf.namelist()

    #     with zipf.open(file_list[0]) as file:
    #         content1 = file.read()
    #     with zipf.open(file_list[1]) as file:
    #         content2 = file.read()

    # # Convert the content to a pandas DataFrame
    # df = pd.read_csv(BytesIO(content1))
    # df_regions=pd.read_csv(BytesIO(content2))
    
    df= pd.read_csv('dataset/athlete_events.csv')
    df_regions= pd.read_csv('dataset/noc_regions.csv')
    df['Medal']=df['Medal'].fillna(0)
    df=df.merge(df_regions,how='left',on='NOC')
    df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],inplace=True)

    df['Year']=df['Year'].astype(int)
    df.drop(['Season','Games'],axis=1,inplace=True)
    
    return df

def medalTally(flagyear='Overall',flagcountries='Overall'):
    df=process_data()
    if flagyear is 'Overall' and flagcountries is 'Overall':
        df= pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
        x = df.groupby('region').agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
        x = x.sort_values(by='Gold', ascending=False)
        x['total']=x['Gold']+x['Silver']+x['Bronze']
        return x
    if flagyear is 'Overall' and flagcountries is not 'Overall':
        df= pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
        df=df[df['region']==flagcountries]
        x = df.groupby('region').agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
        x = x.sort_values(by='Gold', ascending=False)
        x['total']=x['Gold']+x['Silver']+x['Bronze']
        return x
    if flagyear is not 'Overall' and flagcountries is 'Overall':
        df= pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
        df=df[df['Year']==flagyear]
        x = df.groupby('region').agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
        x = x.sort_values(by='Gold', ascending=False)
        x['total']=x['Gold']+x['Silver']+x['Bronze']
        return x
    if flagyear is not 'Overall' and flagcountries is not 'Overall':
        df= pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
        df=df[df['Year']==flagyear]
        df=df[df['region']==flagcountries]
        x = df.groupby('region').agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
        x = x.sort_values(by='Gold', ascending=False)
        x['total']=x['Gold']+x['Silver']+x['Bronze']
        return x

def getvalues():
    df=process_data()
    years=list(df['Year'].sort_values().unique())
    country=list(df['region'].sort_values().unique())
    years.insert(0, 'Overall')
    country.insert(0, 'Overall')
    return years,country

