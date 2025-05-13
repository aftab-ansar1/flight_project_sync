import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv('eda_app_data.csv')

# column = ['Airline', 'Date_of_Journey', 'Source', 'Destination', 'Route',
#        'Dep_Time', 'Arrival_Time', 'Duration', 'Total_Stops',
#        'Additional_Info', 'Price']

c1, c2, c3 = st.columns(3)
with c1:
    source = st.selectbox('Source', df.Source.unique())
    
    info_check = st.checkbox('Additional Info')
    info_selection = st.selectbox('Additional Info', df.Additional_Info.unique())
with c2:
    destination = st.selectbox('Destination', df.Destination.unique())
with c3:
    None
    
df2= df[(df['Source']==source) & (df['Destination']==destination)]

df3 = df2[df2['Additional_Info']==info_selection]
# df3 = pd.DataFrame(df2['Airline'].value_counts())
if st.button('Submit'):
    if df2.empty:
        st.write('No Flights')
    else:
    #     d1, d2 = st.columns(2)
    #     with d1:
    #         if info_check:
    #             st.bar_chart(pd.DataFrame(df3['Airline'].value_counts()))
    #         else:
    #             st.bar_chart(pd.DataFrame(df2['Airline'].value_counts()))
    #     with d2:
    #         if info_check:
    #             st.bar_chart(df3.groupby('Airline')['Price'].mean())
    #         else:
    #             st.bar_chart(df2.groupby('Airline')['Price'].mean())
        df3 = df2.groupby(['stops'])['Price'].mean()
        df4 = df2.groupby(['stops'])['dur_min'].mean()
        st.subheader('Route vs Mean Price Chart')
        st.bar_chart(df2.groupby('Route')['Price'].mean())
        
        st.subheader('Number of Stops vs Mean Price')
        st.bar_chart(df3)
        
        st.subheader('Number of Stops vs Mean Duration in Minutes')
        st.bar_chart(df4)
        
        st.subheader(f'Mean Price by Airlines between {source} and {destination} ')
        st.bar_chart(df2.groupby('Airline')['Price'].mean())
        
        st.subheader(f'Mean Price between {source} and {destination} on Days of Week')
        st.line_chart(df2.groupby('journey_day')['Price'].mean())
        
        st.subheader('Additional Info Available for Airlines')
        df5 =  pd.DataFrame(df2.groupby(['Additional_Info'])['Airline'].value_counts())
        df5



