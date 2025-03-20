import streamlit as st
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Employee Attrition", page_icon="👨‍💼")


@st.cache_resource
def load_model(model_path):
    return joblib.load(model_path)

@st.cache_resource
def load_scaler():
    return joblib.load("scaler.pkl") 


st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
st.sidebar.success("Select The Button")
if st.sidebar.button("💼 Employee Atrrition", use_container_width=True):
    st.session_state.selected_model = "employee_attrition.pkl"


if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
    st.title("🔍 Employee Attrition Analysis")


st.subheader("📌 Business Problem")
st.write("""Employee attrition (employees leaving the company) is a major challenge for businesses.
HR teams struggle to predict which employees are likely to leave, making **proactive retention** difficult
- Increased **recruitment & training costs** 💰  
- Loss of **skilled employees & knowledge** 📉  
- Decreased **team productivity** 📊""")


st.subheader("🔍 Current Solutions")
st.write("""Most companies rely on **manual HR analysis** and **employee surveys** to understand attrition.
- **Time-consuming & labor-intensive** ⏳  
- **Reactive approach** – Action is taken only after employees leave 🏃
- **Human bias & inconsistent insights**  
""")

st.subheader("🚀 Propossed Solution")
st.write("""Our **machine learning model** analyzes employee data to predict **who is at risk of leaving** before they resign.

**Key Benefits:**  
- **🔎 Predict Attrition Early** – Identify employees at risk in advance  
- **⚡ Reduce HR Workload** – Automate attrition analysis instead of manual tracking
- **🏆 Data-Driven Retention** – Help HR create targeted retention strategies
- **💰 Save Hiring Costs** – Retain valuable employees instead of hiring replacements""")


model = load_model(st.session_state.selected_model) if st.session_state.selected_model else None
scaler = load_scaler() if st.session_state.selected_model else None

input_data = []
if st.session_state.selected_model and model:
    st.success(" ### Enter The Employee Details")
    if st.session_state.selected_model == "employee_attrition.pkl":
        feature_1 = abs(st.number_input("Age"))
        feature_2 = abs(st.number_input("Daily Rate"))
        feature_3 = abs(st.number_input("Distance From Home"))
        feature_4 = abs(st.number_input("Gender"))
        feature_5 = abs(st.number_input("Job Satisfaction"))
        feature_6 = abs(st.number_input("Monthly Income"))
        feature_7 = abs(st.number_input("Monthly Rate"))
        feature_8 = abs(st.number_input("Overtime"))
        feature_9 = abs(st.number_input("Percent Salary Hike"))
        feature_10 = abs(st.number_input("Total Working Years"))
        feature_11 = abs(st.number_input("Yearsat Company"))
        input_data = [[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11]]


    if st.button("Predict"):
        input_array = scaler.transform(input_data)
        prediction = model.predict(input_array)[0]

        prediction_label = {
            "Yes": "Employee Will Leave The Company 🏃",
            "No": "Employee Will Not leave The Company 🎯"}

        result = prediction_label.get(prediction)
        st.markdown(f"### Prediction : **{result}**")


# yes - 37, 1373, 2, 1, 3, 2090, 2396, 1, 15, 7, 0
# no - 59, 1324, 3, 0, 1, 2670, 9964, 1, 20, 12, 2