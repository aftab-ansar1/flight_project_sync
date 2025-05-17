#Tables used in the app -- 
# user_data : To store the user input
#interim_table: Copied from the user_data, journey date is dropped and journey time is converted to int type
#interim_table1: copied from the interim_table -- used for making timeseries table for the same input
#interim_table2: copied from the interim_table -- used for making airline series data for the same input
#interim_table 1 and 2 are copied and converted to the input_data1 and input_data2 which is consistent with the training data for the model
#input_data1: used for creating input to the model for the timeseries prediction
#input_data2: used for creating input to the model for the airline series prediction
#End Result: Price prediction of the user input on input date, Price prediction for the user input for consicutive dates (in Line Chart), Price prediction 
# for different airlines on the same day as user input (in bar chart) 

import streamlit as st
import pandas as pd
import numpy as np

# Title of the form
raw_df = pd.read_csv('Flight_price_cleaned_data_2.csv')
st.title("Flight Price Prediction and Passenger Satisfaction Analysis ")

tab1, tab2 = st.tabs(['About', 'Price Prediction'])

with tab1:
    st.subheader('Flight Price Prediction')
    st.write('''The app takes the user input the predicts the price of the flight. The user input fiels are selection boxes with the limited
             number of options. 
             In addition to the Price of the airline for the input journey, the app predicts the price next consicutive days so that the user 
             can plan thir journey efficiently.
             The comparision between the prices of other airlines are also predicted for the comaprison of the user''')

st.subheader('Price Analysis')
st.write('''The app takes the user input As the Source and Destination and gives the Price comparison between different routes, Airlines, number of stops and 
price trend on different days of a week. This app hepls the passenger to effectively analyse the price trends and plan their journey''')

st.subheader('Customer Satisfaction')
st.write('''The App takes the journey details with the passengers rating of Inflight and On-boarding services and predicts the satisfaction of a Customer.
To use the app, fill in all the details and press the submit button. The app will in result gives the Passenger's Satisfaction.
The app is useful Enhancing customer experience by predicting and addressing dissatisfaction.
Providing actionable insights for businesses to improve services.
Supporting marketing teams in identifying target customer groups.
Assisting management in decision-making for customer retention strategies
''')

st.subheader('Customer Satisfaction Insight')
st.write('''TThis page analyse the rating trends of the customers who are Happy and Who are Neutral or Dissatisfied. You can see the ratig trend of different services 
by different age groups. A clear picture emerges from the rating pattern of the customers can be seen.
''')

with tab2:
# Create the form
    form = st.form(key='Price_prediction')

    # Input fields
    airline = form.selectbox("Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet',
        'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia',
        'Vistara Premium economy', 'Jet Airways Business',
        'Multiple carriers Premium economy', 'Trujet'])

    source = form.selectbox("source", ['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai'])
    destination = form.selectbox('destination', ['New Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad'])
    doj = form.date_input('Date of Journey')
    dep_time = form.time_input('dep_time')
    total_stops = form.slider('Total Stops',min_value = 0, max_value = 4)
    additional_info = form.radio('Extra Info',['No Info', 'In-flight meal not included',
        'No check-in baggage included', '1 Short layover',
        '1 Long layover', 'Change airports', 'Business class',
        'Red-eye flight', '2 Long layover'])
    i = form.selectbox('Predict for Days', np.arange(10, 105, 5))
    doj = pd.to_datetime(doj)
    journey_day = doj.dayofweek
    # Form submit button
    submit_button = form.form_submit_button(label='Submit')
    # If the form is submitted
    if submit_button:
        # Create a dictionary with the form data
        form_data = {
            'Airline': airline,
            'Source': source,
            'Destination': destination,
            'Date_of_Journey': doj.date(),
            'journey_day': journey_day,
            'dep_time': dep_time,
            'Total_Stops': total_stops,
            'Additional_Info': additional_info
        }
        
        
        # Convert the dictionary to a DataFrame
        user_data = pd.DataFrame([form_data])
        
        # Display a success message
        st.success("Entry Successful!")
        
        # Display the form data as a table
        st.write("Here are your details:")
        st.table(user_data)
        
        #converting date and time into integer
        interim_table = user_data.copy()
        interim_table = interim_table.drop('Date_of_Journey', axis = 1)
        interim_table['dep_time'] = interim_table['dep_time'].apply(lambda x: int(x.strftime(('%H%M%S'))))
        
        
        interim_table1 = pd.get_dummies(interim_table)
        #input_data_1 is datafraame for the date series for prediction.
        #the date series will generate the same data rows with next dates.
        #the number of rows (dates) will be as per the user input
        input_table1 = pd.DataFrame(columns = ['dur_min', 'stops', 'journey_day', 'dep_time', 'Airline_Air Asia','Airline_Air India',
        'Airline_GoAir', 'Airline_IndiGo', 'Airline_Jet Airways',
        'Airline_Jet Airways Business', 'Airline_Multiple carriers',
        'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
        'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy','Source_Banglore',
        'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai','Destination_Banglore',
        'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
        'Destination_Kolkata', 'Destination_New Delhi','Additional_Info_1 Long layover',
        'Additional_Info_1 Short layover', 'Additional_Info_2 Long layover',
        'Additional_Info_Business class', 'Additional_Info_Change airports',
        'Additional_Info_In-flight meal not included',
        'Additional_Info_No Info',
        'Additional_Info_No check-in baggage included',
        'Additional_Info_Red-eye flight'])
        
        input_table2 = input_table1.copy()
        
        #copying user+table to input_table1 which is consistent with the training data used for the model.
        for col in interim_table1.columns:
            if col in input_table1.columns:
                input_table1[col] = interim_table1[col]
        
        input_table1 = input_table1.fillna(0)
        
        for _ in range (i-1):
            dup_data = input_table1.iloc[-1].to_frame().T
            input_table1=pd.concat([input_table1, dup_data] , ignore_index = True)
            input_table1['journey_day'].iloc[-1] = input_table1['journey_day'].iloc[-1]+1
            
        # input_table1
        ## Creating time series for plot
        # date_series = []
        # for _ in range (i):
        #     next_date = doj+pd.Timedelta(days=1)
        #     next_date = next_date.date()
        #     date_series.append(next_date.strftime("%Y-%m-%d"))
        
        date_series = pd.date_range(start = doj, periods=i, freq = 'D')

        airline = ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet',
        'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia',
        'Vistara Premium economy', 'Jet Airways Business',
        'Multiple carriers Premium economy', 'Trujet']
        interim_table2 = interim_table.copy()
        
        
        for _ in range (len(airline)-1):
            dup_data = interim_table2.iloc[-1].to_frame().T
            interim_table2=pd.concat([interim_table2, dup_data] , ignore_index = True)
        
        interim_table2['Airline'] = airline
        interim_table2[['Total_Stops', 'journey_day', 'dep_time']] = interim_table2[['Total_Stops', 'journey_day', 'dep_time']].astype('int')
        interim_table2 = pd.get_dummies(interim_table2)
        # interim_table2
        
        for col in interim_table2.columns:
            if col in input_table2.columns:
                input_table2[col] = interim_table2[col]    
        input_table2 = input_table2.fillna(0)
        
        # input_table2
        
        # date_series
        import mlflow
        import mlflow.pyfunc

        # mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_tracking_uri("https://dagshub.com/aftab-ansar1/flight_project_sync.mlflow")

        model_name = 'Flight_price_GB_Model'
        model_version = None
        prediction_model = mlflow.pyfunc.load_model(model_uri=f'models:/{model_name}/{model_version}')

        
        #date-wise price prediction
        predicted_price_date = prediction_model.predict(input_table1)
        predicted_price_date = np.round(predicted_price_date,2)
        st.write("Predicted Price", np.round(predicted_price_date[0],2))

        price_series_date = pd.DataFrame({'date': date_series,
                'price':predicted_price_date })
        
        st.line_chart(price_series_date, x = 'date', y = 'price')
        
        predicted_price_flight = prediction_model.predict(input_table2)
        predicted_price_flight = np.round(predicted_price_flight, 2)
        
        flight_rate_df = pd.DataFrame({'Airline':airline,'Price': predicted_price_flight})
        # st.write(flight_rate_df)
        st.bar_chart(data = flight_rate_df, x = 'Airline', y = 'Price')   
    
    
    
    

    
    
    
    
