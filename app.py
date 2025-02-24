import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load("culvert_model.pkl")

# Title of the app
st.title("Box Culvert Cost Estimator")

# Input fields for the 10 variables
clear_length = st.number_input("Clear Length (m)", min_value=0.0, step=0.1)
height = st.number_input("Height (m)", min_value=0.0, step=0.1)
soil_height = st.number_input("Soil Height Above Slab (m)", min_value=0.0, step=0.1)
num_cells = st.number_input("Number of Cells", min_value=1, step=1)
total_length = st.number_input("Total Length (m)", min_value=0.0, step=0.1)
zone = st.selectbox("Zone", options=[1, 2, 3, 4, 5])  # Adjust based on your dataset
year = st.number_input("Year", min_value=2000, max_value=2030, step=1)

# Predict button
if st.button("Estimate Cost"):
    input_data = np.array([[clear_length, height, soil_height, num_cells, total_length, zone, year, var_8, var_9, var_10]])
    predicted_cost = model.predict(input_data)[0]
    st.success(f"Estimated Cost: ${predicted_cost:,.2f}")
