import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load("culvert_model.pkl")

# Title of the app
st.title("ESTIMACION COSTO CAJÓN PLUVIAL")


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Cajon Pluvial", "Tuberías", "Movimientos de tierra", "Bardas", "Muros de contención"])

with tab1:
    st.header("CAJON PLUVIAL")
    st.write("Content for the first tab.")
    st.image("cajon.png", caption="Ejemplo", use_container_width=True)
    
    # Input fields for the 10 variables
    clear_length = st.number_input("Claro Libre (m)", min_value=0.0, step=0.1)
    height = st.number_input("Altura (m)", min_value=0.0, step=0.1)
    soil_height = st.number_input("Colchon (m)", min_value=0.0, step=0.1)
    num_cells = st.number_input("Celdas", min_value=1, step=1)
    total_length = st.number_input("Longitud(m)", min_value=0.0, step=0.1)
    zone = st.number_input("Zona (Km al proyecto a partir de Terra)", min_value=0.0, max_value=100.0, step=0.1)
    year = st.number_input("Año", min_value=2021, max_value=2026, step=1)
    
    # Predict button
    if st.button("Estimate Cost"):
        input_data = np.array([[clear_length, height, soil_height, num_cells, total_length, zone, year]])
        predicted_cost = model.predict(input_data)[0]
        st.success(f"Estimated Cost: ${predicted_cost:,.2f}")
        
with tab2:
    st.header("This is Tab 2")
    st.write("Content for the second tab.")

with tab3:
    st.header("This is Tab 3")
    st.write("Content for the third tab.")

with tab4:
    st.header("This is Tab 3")
    st.write("Content for the third tab.")

with tab5:
    st.header("This is Tab 3")
    st.write("Content for the third tab.")



