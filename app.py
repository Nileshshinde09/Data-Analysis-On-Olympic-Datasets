import streamlit as st
import pandas as pd
import handler
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
menu=st.sidebar.radio(
    'Selected an Option',
    ('Medal Tally','Overall Analysis','Athlete wise Alaysis')
)
if menu=='Medal Tally':
    years,countries=handler.getvalues()
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    if selected_year is 'Overall' and selected_country is 'Overall':
        st.header("Overall Medal Tally")
    if selected_year is 'Overall' and selected_country is not 'Overall':
        st.header(f"Overall Years Medal Tally Of {selected_country}")
    if selected_year is not 'Overall' and selected_country is 'Overall':
        st.header(f"Year {selected_year} Olympics Medal Tally Of Overall Countries")
    if selected_year is not 'Overall' and selected_country is not 'Overall':
        st.header(f"Year {selected_year} Olympics Medal Tally Of {selected_country}")
    st.table(data=handler.medalTally(selected_year,selected_country))

if menu=='Overall Analysis':
    df=pd.read_pickle("maindf.pkl") 
    edition=len(df['Year'].unique())
    host=len(df['City'].unique())
    sports=len(df['Sport'].unique())
    events=len(df['Event'].unique())
    athletes=len(df['Name'].unique())
    nations=len(df['region'].unique())

    st.title("Top Statastics")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.header("Edition")
        st.title(edition)
    with c2:
        st.header("Host")
        st.title(host)
    with c3:
        st.header("Sports")
        st.title(sports)


    c1,c2,c3 = st.columns(3)
    with c1:
        st.header("Events")
        st.title(events)
    with c2:
        st.header("Athletes")
        st.title(athletes)
    with c3:
        st.header("Nations")
        st.title(nations)

    
    st.table(df)
    # nations_over_time =df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('index')

    # nations_over_time.rename(columns={'index': 'Edition', 'Year': 'region'}, inplace=True)
    # fig = px.line(nations_over_time, x="Edition", y="region")
    # st.title("Participating Nations over the years")
    # st.plotly_chart(fig)

    
    # st.title("Athletes over the years")
    # athlete_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('index')
    # athlete_over_time.rename(columns={'index': 'Edition', 'Year': 'Athlete'}, inplace=True)
    # fig = px.line(athlete_over_time, x="Edition", y="Athlete")
    # st.plotly_chart(fig)

    
    # st.title("No. of Events over time(Every Sport)")
    # fig,ax = plt.subplots(figsize=(20,20))
    # x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    # ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    # st.pyplot(fig)

if menu=='Athlete wise Alaysis':
    df=pd.read_pickle("maindf.pkl") 
    st.title("Distribution of Age")
    new_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = new_df['Age'].dropna()
    x2 = new_df[new_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = new_df[new_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = new_df[new_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)



    x=[]
    name=[]
    famous_sports=df['Sport'].value_counts().head(39).to_frame().index
    for sport in famous_sports:
        temp=df[df['Sport']==sport]
        x.append(temp[temp['Medal']=='Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age w.r.t Sports(Gold Medalist)")
    st.plotly_chart(fig)



    st.title('Height Vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    new_df = df.drop_duplicates(['Name', 'region'])
    new_df['Medal'].fillna('No Medal', inplace=True)
    selectedsport=st.selectbox('Select a Sport',sport_list)
    if selectedsport is 'Overall':
        temp=new_df
    if selectedsport is not 'Overall':
        temp=new_df[new_df['Sport']==selectedsport]
    # temp = handler.weightVheightt(selectedsport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp['Weight'],temp['Height'],hue=temp['Medal'],style=temp['Sex'],s=60)
    st.pyplot(fig)


    st.title("Men Vs Women Participation Over the Years")
    athlete_df = df.drop_duplicates(['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
