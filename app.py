import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load("culvert_model.pkl")

# Initialize session state for storing multiple estimates
if "culvert_estimates" not in st.session_state:
    st.session_state.culvert_estimates = []



# Title of the app
st.title("ESTIMACIÓN DE COSTOS DE URBANIZACION")


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Cajon Pluvial", "Tuberías", "Movimientos de tierra", "Bardas", "Muros de contención", "RESUMEN"])

with tab1:
    st.header("CAJON PLUVIAL")
    st.write("Content for the first tab.")
    st.image("cajon.png", caption="Ejemplo", use_container_width=True)
    
    # Input fields for the 10 variables
    culvert_name = st.text_input("Enter Culvert Name", value="Culvert 1")
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
        estimated_cost = model.predict(input_data)[0]
        # Save to session state as a dictionary
        st.session_state.culvert_estimates.append({"name": culvert_name, "cost": estimated_cost})
        st.success(f"Saved {culvert_name} with Cost: ${estimated_cost}")
        
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

with tab6:
    st.header("This is Tab 3")
    st.write("Content for the third tab.")

    if st.session_state.culvert_estimates:
        # Display saved culverts
        for i, estimate in enumerate(st.session_state.culvert_estimates):
            st.write(f"**{i+1}. {estimate['name']}** - Cost: **${estimate['cost']}**")

        # Clear all estimates
        if st.button("Clear All Estimates"):
            st.session_state.culvert_estimates = []
            st.warning("All estimates have been cleared!")
    else:
        st.warning("No estimates saved yet.")

