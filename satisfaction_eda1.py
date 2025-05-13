import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import streamlit as st

df = pd.read_csv('satisfaction_data.csv')

Passenger_info = ['Gender', 'Age','Type of Travel', 'Class']

travel_info = ['Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes' ]


inflight_service = ['Inflight wifi service','Food and drink','Seat comfort','Inflight entertainment','Leg room service', 'Inflight service',
       'Cleanliness']

boarding_service = ['Departure/Arrival time convenient', 'Ease of Online booking',
       'Gate location', 'Online boarding', 'On-board service', 'Baggage handling', 'Checkin service',] 

age_groups = {'FGroup' : [1, 2, 3, 4, 5, 6],
             'Min Age': [7, 13, 20, 36, 51, 66], 
             'Max Age': [12, 19, 35, 50, 65, 85]
}




# selection = st.selectbox("Select Category",['Gender','Customer Type', 'Type of Travel', 'Class'] )

# st.subheader('Summary Table of Passenger Satisfaction')
# df1 = df.groupby(['satisfaction','Gender','Customer Type', 'Type of Travel'])['Class'].value_counts(normalize = True)

# df1 = df1.reset_index()
# df1

st.subheader('Passenger Satisfaction by Gender')
df0 = pd.pivot_table(data=df, index = 'Gender', columns = 'satisfaction', aggfunc = 'count')['Age'].reset_index()
c1, c2 = st.columns(2)
with c1:
       st.bar_chart(df0, x = 'Gender', y = 'neutral or dissatisfied')
with c2:
       st.bar_chart(df0, x = 'Gender', y = 'satisfied')
df0

st.subheader('Passenger Satisfaction by Travel Class')
df00 = pd.pivot_table(data=df, index = 'Class', columns = 'satisfaction', aggfunc = 'count')['Age'].reset_index()
c3, c4 = st.columns(2)
with c3:
       st.bar_chart(df00, x = 'Class', y = 'neutral or dissatisfied')
with c4:
       st.bar_chart(df00, x = 'Class', y = 'satisfied')
df00




st.subheader('Listed services in the data of the passenger')
c1, c2, c3 = st.columns(3)
with c1:
       st.write('Inflight Services')
       st.write(pd.DataFrame(data = inflight_service, columns = ['inflight_services']))
with c2:
       st.write('Boarding Services')
       st.write(pd.DataFrame(data = boarding_service, columns = ['boarding_services']))
with c3:
       st.write('Age Group')
       st.write(pd.DataFrame(age_groups))

st.subheader('Average Rating of Boarding Services by Different Age Groups')
st.write("By Female Passengers")
df2 = df[df['Gender']=='Female'].groupby('age_group')[boarding_service].mean()
df2.reset_index()
st.bar_chart(df2, stack = False)
st.image('output.png')

st.write("By Male Passengers")
df3 = df[df['Gender']=='Male'].groupby('age_group')[boarding_service].mean()
df3.reset_index()
st.bar_chart(df3, stack = False)
st.image('output1.png')

st.subheader('Colclusion for Boarding Services ratings for different age groups')
st.write(''''1. Gate Location' is ALMOST UNIFORMALLY RATED' between all age groups.  
2. Rating pattern of 'Departure and Arrival Time' in both Male and Female Passengers is same.  
3. Rating pattern of 'Ease of Online Booking' in both Male and Female Passengers is same.   
4. Male Passengers in age group 5 have given lover ratings to 'Online Boarding' than the Female passengers in the same group. This shows the Females in age group 5 are not doing online boarding by themselves and are assisted by someone.        
5. Rating pattern of 'Onboard Servises' in both Male and Female Passengers is same.   
6. Bagage handling in Females of age-group 3 to 6 are inconvennient.  
7. Checkin Services in Females of age-group 2 are little bit more inconvenient.''')

st.divider()

st.subheader("Average Rating of Inflight Services by different Age Groups") 

st.write("by Female Passengers")
df4 = df[df['Gender']=='Female'].groupby('age_group')[inflight_service].mean()
df4.reset_index()
st.bar_chart(df4, stack = False)
st.image('output3.png')

st.write("By male Passengers")
df5 = df[df['Gender']=='Male'].groupby('age_group')[inflight_service].mean()
df5.reset_index()
st.bar_chart(df5, stack = False)
st.image('output3.png')

st.subheader('Colclusion for Inflight Services ratings for different age groups')
st.write('''
Inflight WiFi Service: Female passengers tend to rate WiFi service slightly higher than males across all age groups, though scores remain low for both genders.

Food and Drink: Female passengers generally give better ratings for food and drink compared to males, especially in older age groups.

Seat Comfort: Female passengers in older age groups (5 and 6) rate seat comfort much higher than male passengers, indicating better satisfaction.

Inflight Entertainment: Male passengers rate inflight entertainment slightly higher across all age groups, whereas female passengers experience a noticeable dip in satisfaction in group 6.

Leg Room Service: Male passengers in middle age groups (4 and 5) rate legroom better, whereas females in group 6 report significantly lower ratings.

Inflight Service: Both genders rate inflight service highly, though male passengers display more consistency across all age groups.

Cleanliness: Female passengers provide slightly higher ratings for cleanliness overall, with middle-aged women (5) showing the highest satisfaction.  

Female passengers tend to rate food, seat comfort, and cleanliness higher than males, suggesting a greater appreciation for service quality.

Male passengers express higher satisfaction with inflight entertainment and legroom, particularly in middle age groups.''')

st.subheader("Overall rating Trend")

st.write('Rating Trend for Inflight Services')
st.image('output5.png')
st.write('\n')
st.write('\n')
st.write('\n')

st.write('Rating Trend for Boarding Services')
st.image('output6.png')

st.write("All services rated by the neutral or dissatisfied passengers are rated below the average rating of the services")

st.subheader('Comprehensive Report on Age Group and Passenger Stisfaction')
for i in range (1, 7):
       st.write(f'Age_group {i}')
       st.write(f'Age: {df[df['age_group']==i]['Age'].min()} to {df[df['age_group']==i]['Age'].max()}')
       dff = pd.DataFrame(df[df['age_group']==i]['satisfaction'].value_counts(normalize = True))
       dff['Proportion of Total'] = (df[df['age_group']==i]['satisfaction'].value_counts()/df.shape[0])
       dff
       st.bar_chart(df[df['age_group']==i]['satisfaction'].value_counts(normalize = True))
       st.write('----------------------------------------')