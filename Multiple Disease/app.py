import streamlit as st
import numpy as np
import joblib
import logging


st.set_page_config(page_title="ML Model Selector", page_icon="🤖")

st.sidebar.success("Select a model for prediction")
st.markdown("# 🤖 ML Model Selector")

@st.cache_resource
def load_model(model_path):
    model = joblib.load(model_path)
    return model
    

# Initialize session state
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
    st.markdown("## Kidney Disease")
    st.write("Kidney disease happens when the kidneys can't filter waste properly. This leads to toxin buildup in the body, causing swelling, fatigue, and high blood pressure. Common causes include diabetes, high blood pressure, and infections.")

    st.markdown("## Liver Disease")
    st.write("Liver disease affects the liver's ability to remove toxins and digest food. It can be caused by alcohol, hepatitis, or fatty liver. Symptoms include jaundice, swelling, and fatigue.")

    st.markdown("## Parkinson's Disease")
    st.write("Parkinson's is a brain disorder that affects movement and coordination. It causes tremors, stiffness, and slow movement over time. The disease is due to a lack of dopamine in the brain.")

# Sidebar Buttons for Model Selection
if st.sidebar.button("🧬 Kidney Prediction", use_container_width=True):
    st.session_state.selected_model = "kidney_model.pkl"
if st.sidebar.button("🫀 Liver Prediction", use_container_width=True):
    st.session_state.selected_model = "liver_model.pkl"
if st.sidebar.button("🧠 Parkinson's Prediction", use_container_width=True):
    st.session_state.selected_model = "parkinsons_model.pkl"

# Load selected model
model = load_model(st.session_state.selected_model) if st.session_state.selected_model else None

# Define different input fields for each model
input_data = []
if st.session_state.selected_model and model:
    st.markdown(f"## Selected Model : `{st.session_state.selected_model}`")

    if st.session_state.selected_model == "kidney_model.pkl":
        feature_1 = abs(st.number_input("Blood Pressure"))
        feature_2 = abs(st.number_input("Specific Gravity"))
        feature_3 = abs(st.number_input("Albumin"))
        feature_4 = abs(st.number_input("Blood Urea"))
        feature_5 = abs(st.number_input("Sodium"))
        feature_6 = abs(st.number_input("Potassium"))
        feature_7 = abs(st.number_input("hemoglobin"))
        feature_8 = abs(st.number_input("diabetes mellitus"))
        input_data = [[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8]]

    elif st.session_state.selected_model == "liver_model.pkl":
        feature_1 = abs(st.number_input("Age"))
        feature_2 = abs(st.number_input("Total_Bilirubin"))
        feature_3 = abs(st.number_input("Direct_Bilirubin"))
        feature_4 = abs(st.number_input("Alkaline_Phosphotase"))
        feature_5 = abs(st.number_input("Alamine_Aminotransferase"))
        feature_6 = abs(st.number_input("Aspartate_Aminotransferase"))
        feature_7 = abs(st.number_input("Total_Protiens"))
        feature_8 = abs(st.number_input("Albumin"))
        feature_9 = abs(st.number_input("Albumin_and_Globulin_Ratio"))
        input_data = [[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9]]

    elif st.session_state.selected_model == "parkinsons_model.pkl":
        feature_1 = abs(st.number_input("MDVP_Fo(Hz)"))
        feature_2 = abs(st.number_input("MDVP_Flo(Hz)"))
        feature_3 = abs(st.number_input("Shimmer_APQ5"))
        feature_4 = abs(st.number_input("MDVP_APQ"))
        feature_5 = abs(st.number_input("HNR"))
        feature_6 = abs(st.number_input("Spread2"))
        feature_7 = abs(st.number_input("PPE"))
        input_data = [[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7]]

    # Prediction button
    if st.button("Predict"):
        input_array = np.array(input_data)
        prediction = model.predict(input_array)[0]

        prediction_labels = {
            "ckd": "Chronic Kidney Disease ⚠️",
            "notckd": "No Kidney Disease 😊",
            1 : "Liver Disease Detected ⚠️",
            0 : "No Liver Disease 😊",
            2 : "Parkinson's Disease ⚠️",
            3 : "No Parkinson's Disease 😊"
        }

        result = prediction_labels.get(prediction)
        st.markdown(f"### Prediction : **{result}**")