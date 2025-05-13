import streamlit as st
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

selection_range = np.arange(1, 6, 1)
# Title of the form
st.title("Customer Rating Predictor")
# Create the form
with st.form(key='Customer Rating Predictor'):
# Input fields
    st.subheader('Enter Passenger Info')
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        age = st.number_input("Customer Age", min_value=7, max_value=100, step = 1)
        Gender = st.selectbox("Gender", ['Male', 'Female'])
    with c2:
        cus_type = st.selectbox("Customer Type", ['Loyal Customer', 'disloyal Customer'])
        flight_distance = st.number_input("Flight Distance in Km", min_value=200, max_value = 100000, step=50)
    
    with c3:
        travel_type = st.selectbox("Travel Type", ["Personal Travel", "Business travel"])
        delay = st.number_input("Departure Delay (Min)", min_value=0, max_value=3000, step=1)
    
    with c4:
        clas = st.selectbox("Class", ['Business', 'Eco', 'Eco Plus'])
    
    
    
    c5, c6= st.columns(2)
    with c5:
        st.subheader('Rate Boarding Services')
        Ease_of_Online_booking = st.selectbox("Ease of Online Booking", selection_range)
        Online_boarding = st.selectbox("Online Boarding", selection_range)
        Baggag_handling = st.selectbox("Baggage Handling", selection_range)
        Checkin_service = st.selectbox("Checkin", selection_range)
        Onboard_service = st.selectbox("On-board service", selection_range)
        Gate_location = st.selectbox("Gate location", selection_range)
        time_convenient = st.selectbox("Time Convenient", selection_range)
    
    with c6:
        st.subheader('Rate the Inflight Services')
        Seat_comfort = st.selectbox("Seat comfort", selection_range)
        Leg_room_service = st.selectbox("Leg room service", selection_range)
        inflight_entertainment = st.selectbox("Inflight entertainment", selection_range)
        Food_and_drink = st.selectbox("Food & Drink", selection_range)
        
        Cleanliness = st.selectbox("Cleanliness", selection_range)
        wifi_service = st.selectbox("In-Flight WiFi Service", selection_range)
        inflight_service = st.selectbox("Inflight service", selection_range)
    
    submit_button = st.form_submit_button(label='Submit')
# # If the form is submitted
if submit_button:
    # Create a dictionary with the form data
    form_data = {
        'Age': age,
        'Flight Distance': flight_distance,
        'Inflight wifi service': wifi_service,
        'Departure/Arrival time convenient': time_convenient,
        'Ease of Online booking': Ease_of_Online_booking,
        'Gate location': Gate_location,
        'Food and drink':Food_and_drink,
        'Online boarding':Online_boarding,
        'Seat comfort':Seat_comfort,
        'Inflight entertainment':inflight_entertainment,
        'On-board service':Onboard_service,
        'Leg room service':Leg_room_service,
        'Baggage handling':Baggag_handling,
        'Checkin service':Checkin_service,
        'Inflight service':inflight_service,
        'Cleanliness':Cleanliness,
        'Departure Delay in Minutes':delay,
        'Class':clas,
        'Gender':Gender,
        'Customer Type':cus_type,
        'Type of Travel':travel_type
    }
    
#     # Convert the dictionary to a DataFrame
    df = pd.DataFrame([form_data])
    
#     # Display a success message
    st.success("Entry Successful")
    
#     # Display the form data as a table
    st.write("Here are your details:")
    st.dataframe(df)
    
    next_data = df.copy()
    for _ in range (2):
        df = pd.concat([df, next_data], axis = 0, ignore_index=True)
    
    if Gender == 'Male':
        df.loc[1, 'Gender'] = 'Female' 
    else:
        df.loc[1, 'Gender'] = 'Male'
    
    if cus_type == 'Loyal Customer':
        df.loc[1, 'Customer Type'] = 'disloyal Customer' 
    else:
        df.loc[1, 'Customer Type'] = 'Loyal Customer'
    
    if travel_type == 'Business travel':
        df.loc[1,'Type of Travel'] = 'Personal Travel'
    else:
        df.loc[1,'Type of Travel'] = 'Business Travel'
    
    if clas == 'Eco':
        df.loc[1, 'Class'] = 'Business'
        df.loc[2, 'Class'] = 'Eco Plus'
    elif clas == 'Eco Plus':
        df.loc[1, 'Class'] = 'Business'
        df.loc[2, 'Class'] = 'Eco'
    else:
        df.loc[1, 'Class'] = 'Eco'
        df.loc[2, 'Class'] = 'Eco Plus'
    
    #Plotting Service Charts
        
        inflight_service = {
        'Inflight wifi service': wifi_service,
        'Food and drink':Food_and_drink,
        'Seat comfort':Seat_comfort,
        'Inflight entertainment':inflight_entertainment,
        'Leg room service':Leg_room_service,
        'Inflight service':inflight_service,
        'Cleanliness':Cleanliness,
    }

    
    Boarding_service = {
        
        'Ease of Online booking': Ease_of_Online_booking,
        'Gate location': Gate_location,
        'Online boarding':Online_boarding,
        'On-board service':Onboard_service,
        'Baggage handling':Baggag_handling,
        'Checkin service':Checkin_service,
        'Departure/Arrival time convenient': time_convenient
    }
    d1, d2 = st.columns(2)
    with d1:
        st.line_chart(inflight_service)
    with d2:
        st.line_chart(Boarding_service)
    #Date Pipeline
    df = pd.get_dummies(df, columns=['Class'], dtype = int)
    df = pd.get_dummies(df, drop_first=True, dtype = int)
    
    
    mlflow.set_tracking_uri("http://localhost:5000")
    #st.table(df)
    model_name = 'customer_prediction_RF_model'
    version = None 
    run_id = '3d6a4e8dd6db400dacd586b5518420d0'
    
    import time

    with st.spinner('Wait for it...'):
        time.sleep(5)
    
    #import pyfunc
    prediction_model = mlflow.pyfunc.load_model(model_uri=f'models:/{model_name}/{version}')
    predicted_rating = prediction_model.predict(df)
    if predicted_rating[0] == 1:
        st.subheader('Happy Customer :blush:')
    else:
        st.subheader('Neutral or Dissatisfied :expressionless:')
    