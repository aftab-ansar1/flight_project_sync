import streamlit as st



pg = st.navigation([
    st.Page("Price_APP.py", title="Price Prediction", icon="🔥"),
    st.Page("eda_price.py", title = 'Price Analysis', icon = "📉"),
    st.Page("app2.py", title="Customer Satisfaction", icon="💯"),
    st.Page('satisfaction_eda1.py', title = 'Customer Satisfaction Insights', icon = '🔢')
])
pg.run()