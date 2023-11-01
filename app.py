import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import handler

menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Athlete-wise Analysis')
)

if menu == 'Medal Tally':
    years, countries = handler.getvalues()
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)

    st.header("Medal Tally")
    st.table(data=handler.medalTally(selected_year, selected_country))

if menu == 'Overall Analysis':
    df = pd.read_csv('maindf.csv')
    edition = len(df['Year'].unique())
    host = len(df['City'].unique())
    sports = len(df['Sport'].unique())
    events = len(df['Event'].unique())
    athletes = len(df['Name'].unique())
    nations = len(df['region'].unique())

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Edition")
        st.title(edition)

    with col2:
        st.header("Host")
        st.title(host)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Athletes")
        st.title(athletes)

    with col3:
        st.header("Nations")
        st.title(nations)

    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
    nations_over_time.rename(columns={'index': 'Edition', 'Year': 'region'}, inplace=True)

    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig)

    athlete_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index()
    athlete_over_time.rename(columns={'index': 'Edition', 'Year': 'Athlete'}, inplace=True)

    fig = px.line(athlete_over_time, x="Edition", y="Athlete")
    st.title("Athletes Over the Years")
    st.plotly_chart(fig)

    st.title("No. of Events Over Time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True
    )
    st.pyplot(fig)

if menu == 'Athlete-wise Analysis':
    df = pd.read_csv('maindf.csv')

    st.title("Distribution of Age")
    new_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = new_df['Age'].dropna()
    x2 = new_df[new_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = new_df[new_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = new_df[new_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = df['Sport'].value_counts().head(39).to_frame().index

    for sport in famous_sports:
        temp = df[df['Sport'] == sport]
        x.append(temp[temp['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age w.r.t Sports (Gold Medalist)")
    st.plotly_chart(fig)

    st.title('Height Vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    new_df = df.drop_duplicates(['Name', 'region'])
    new_df['Medal'].fillna('No Medal', inplace=True)
    selected_sport = st.selectbox('Select a Sport', sport_list)

    if selected_sport == 'Overall':
        temp = new_df
    else:
        temp = new_df[new_df['Sport'] == selected_sport]

    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp['Weight'], temp['Height'], hue=temp['Medal'], style=temp['Sex'], s=60)
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
