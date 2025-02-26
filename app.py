import streamlit as st
import joblib
import numpy as np
import pandas as pd
import mathplotlib as plt

# Load the trained model
model = joblib.load("culvert_model.pkl")


# Set a password (you can change this)
PASSWORD = "terra"


# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login Form
if not st.session_state.authenticated:
    st.title("Login Page")
    password_input = st.text_input("Enter Password:", type="password")
    
    if st.button("Login"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True  # Unlock the app
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")




### acciones si se ingresa contraseña correcta
if st.session_state.authenticated:
    


    # Initialize session state for storing multiple estimates
    if "culvert_estimates" not in st.session_state:
        st.session_state.culvert_estimates = []
    
    # Title of the app
    st.title("ESTIMACIÓN DE COSTOS DE URBANIZACION")

### guadar info de cada tab
    def save_estimate(culvert_type, estimated_cost, name):

    # Save data to session state with the type of culvert
        st.session_state.culvert_estimates.append({
            "name": name,
            "type": culvert_type,  # Store the type from the tab
            "P.U": estimated_cost,
            "Cantidad": 1,  # Default quantity (editable in summary tab)
            "Subtotal": estimated_cost*1
        })
    
        st.success(f"Saved {name} ({culvert_type}) with Cost: ${estimated_cost}")
    

    
    
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
            estimated_cost = round(model.predict(input_data)[0], 2)
            save_estimate("Pluvial", estimated_cost, culvert_name)
    
    
    
            
    

    
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


        if st.button("Refresh"):
            st.rerun()
    
        if st.session_state.culvert_estimates:
            # Convert to DataFrame
            df = pd.DataFrame(st.session_state.culvert_estimates)
    
            # Make table editable
            edited_df = st.data_editor(df, num_rows="dynamic", key="estimates_table")
    
            
            # Update session state with edited values
            st.session_state.culvert_estimates = edited_df.to_dict("records")  

                    
            for item in st.session_state.culvert_estimates:
                item["Subtotal"] = item["P.U"] * item["Cantidad"]
    
            # Remove selected rows
            #if any(item["delete"] for item in st.session_state.culvert_estimates):
             #   st.session_state.culvert_estimates = [
              #      item for item in st.session_state.culvert_estimates if not item["delete"]
               # ]
                #st.experimental_rerun()  # Refresh the page after deletion
    
            # Calculate final cost
            df["final_cost"] = df["P.U"] * df["Cantidad"]
    
            # Display updated table
            #st.write("Updated Estimates Table:")
            #st.dataframe(edited_df)
    
    
            # Show total cost
            total_cost = df["final_cost"].sum()
            st.subheader(f"Costo total urbanización: ${total_cost}")
            
    
            # Clear all estimates
            if st.button("Clear All Estimates"):
                st.session_state.culvert_estimates = []
                st.warning("All estimates have been cleared!")
                st.rerun()

            
                
            updated_df = pd.DataFrame(st.session_state.culvert_estimates)
            
                # === PIE CHART: COST PER TYPE ===
            st.subheader("Cost Distribution by Culvert Type")
    
            # Group by "type" and sum the subtotals
            type_totals = updated_df.groupby("type")["Subtotal"].sum()
    
            if not type_totals.empty:
                # Create Pie Chart
                fig, ax = plt.subplots()
                ax.pie(type_totals, labels=type_totals.index, autopct="%1.1f%%", startangle=90, colors=["#ff9999","#66b3ff","#99ff99"])
                ax.axis("equal")  # Equal aspect ratio ensures pie is circular
    
                # Display Pie Chart in Streamlit
                st.pyplot(fig)
            else:
                st.warning("No data available for pie chart.")
    
        
        else:
            st.warning("No estimates saved yet.")
            
        # Logout button
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
