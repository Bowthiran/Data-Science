import os
import joblib
import re
import numpy as np
import streamlit as st
import docx
import pdfplumber
import tempfile
from googletrans import Translator
from textblob import TextBlob
from transformers import pipeline
from sklearn.preprocessing import FunctionTransformer
from sentence_transformers import SentenceTransformer


st.set_page_config(page_title="Insurance AI", page_icon="🎗️")
st.sidebar.success("Select a model to explore")

@st.cache_resource
def load_model(model_path):
    model = joblib.load(model_path)
    return model


#Multilingual Model
def extract_text_and_translate(file_path, src_lang="en", dest_lang="en"):
    ext = os.path.splitext(file_path)[-1].lower()
    translator = Translator()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif ext == ".docx":
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    else:
        raise ValueError("❌ Unsupported file type!")

    lines = text.split("\n")
    translated = [translator.translate(line, src=src_lang, dest=dest_lang).text for line in lines if line.strip()]
    return "\n".join(translated)


# Sentiment Analysis Model
def sentiment_analysis(raw_text):
    stop_words = set([
        'the', 'and', 'is', 'in', 'it', 'of', 'to', 'a', 'for', 'on', 'this', 'that', 'with',
        'as', 'was', 'but', 'are', 'have', 'be', 'at', 'or', 'an', 'so', 'if', 'out', 'not'])

    raw_text = " ".join(raw_text) if isinstance(raw_text, list) else raw_text
    lower = raw_text.lower()
    special = re.sub(r"[^a-zA-Z0-9]", " ", lower)
    tokens = special.split()
    tokens = [word for word in tokens if word not in stop_words]
    text = " ".join(tokens)

    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"


# Text Summazation Model
def summarize_text(text):
    # device = 0 if torch.cuda.is_available() else -1
    summarizer = pipeline("summarization", model="t5-small")
    summary = summarizer(text, max_length=100, min_length=25, do_sample=False)
    return summary[0]["summary_text"]


# Chatbot Model
chatbot_model = joblib.load("C:/Users/91801/Desktop/Insurance Project/models/chatbot_model.pkl")
qa_pairs = chatbot_model["qa_pairs"]
question_embeddings = chatbot_model["question_embeddings"]
sentence_model = SentenceTransformer(chatbot_model["model_name"])
def get_best_answer(user_question):
    user_embedding = sentence_model.encode([user_question])[0]
    similar = np.dot(question_embeddings, user_embedding)
    best_index = np.argmax(similar)
    return qa_pairs[best_index]["answer"]



if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
    st.markdown("# 🤖 Insurance AI Hub")
    st.markdown("### 🔐 Risk Classification")
    st.write("Classifies insurance applicants based on potential risk levels using historical and behavioral data. Helps insurers make smarter underwriting decisions and reduce potential losses.")

    st.markdown("### 💵 Claim Amount")
    st.write("Estimates the expected claim amount from a policyholder based on input features like age, damage type, and history. Useful for cost planning and fraud prevention in insurance claims.")

    st.markdown("### 👥 Customer Segmentation")
    st.write("Groups customers into meaningful segments based on demographics, policy behavior, and engagement. Supports targeted marketing, policy customization, and service optimization.")

    st.markdown("### 🚨 Frud Detection")
    st.write("Identifies suspicious or potentially fraudulent claims by analyzing patterns and anomalies in the data. Enhances the integrity of insurance processes and minimizes financial loss.")

    st.markdown("### 🌐 Insurance Translate")
    st.write("Translates insurance related documents or messages across different languages. Improves communication with diverse customer bases and enhances accessibility.")

    st.markdown("### 💭 Sentiment Analysis")
    st.write("Analyzes customer feedback, emails, or reviews to detect sentiment. Helps in measuring customer satisfaction, resolving issues faster, and improving service quality.")

    st.markdown("### 📝 Text Summarization")
    st.write("Automatically summarizes long insurance documents, policies, or claim descriptions. Saves time and improves document readability for agents and customers.")

    st.markdown("### 🌀 Chatbot Assistant")
    st.write("Provides instant responses to insurance related queries using natural language understanding. Enhances customer experience with 24/7 support and reduces human workload.")


# Sidebar Buttons for Model Selection
if st.sidebar.button("⚠️ Risk Classification", use_container_width=True):
    st.session_state.selected_model = "C:/Users/91801/Desktop/Insurance Project/models/risk_classification.pkl"
if st.sidebar.button("💰 Claim Amount", use_container_width=True):
    st.session_state.selected_model = "C:/Users/91801/Desktop/Insurance Project/models/claim_amount.pkl"
if st.sidebar.button("🧩 Customer Segment", use_container_width=True):
    st.session_state.selected_model = "C:/Users/91801/Desktop/Insurance Project/models/customer_segmentation.pkl"
if st.sidebar.button("🕵️‍♂️ Fraud Detection", use_container_width=True):
    st.session_state.selected_model = "C:/Users/91801/Desktop/Insurance Project/models/fraud_detection.pkl"
if st.sidebar.button("🌍 Insurance Translate", use_container_width=True):
    st.session_state.selected_model = "C:/Users/91801/Desktop/Insurance Project/models/insurance_translate.pkl"
if st.sidebar.button("❤️ Sentiment Analysis", use_container_width=True):
    st.session_state.selected_model = "C:/Users/91801/Desktop/Insurance Project/models/sentiment_analysis.pkl"
if st.sidebar.button("📝 Text Summarization", use_container_width=True):
    st.session_state.selected_model = "C:/Users/91801/Desktop/Insurance Project/models/text_summarization.pkl"
if st.sidebar.button("🤖 Chatbot", use_container_width=True):
    st.session_state.selected_model = "C:/Users/91801/Desktop/Insurance Project/models/chatbot_model.pkl"


# Load selected model
model = load_model(st.session_state.selected_model) if st.session_state.selected_model else None

# Define different input fields for each model
input_data = [] 
if st.session_state.selected_model and model:
    if st.session_state.selected_model == "C:/Users/91801/Desktop/Insurance Project/models/risk_classification.pkl":
        st.title("🧠 Risk Classification")
        feature_1 = abs(st.number_input("Customer Age"))
        feature_2 = abs(st.number_input("Annual Income"))
        feature_3 = abs(st.number_input("Property Age"))
        feature_4 = abs(st.number_input("Claim History"))
        feature_5 = abs(st.number_input("Premium Amount"))
        feature_6 = abs(st.number_input("Claim Amount"))
        feature_7 = abs(st.number_input("Fraudulent Claim"))
        feature_8 = abs(st.number_input("Gender Male"))
        feature_9 = abs(st.number_input("Health Policy"))
        feature_10 = abs(st.number_input("Life policy"))
        feature_11 = abs(st.number_input("Property policy"))
        input_data = [[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11]]

    elif st.session_state.selected_model == "C:/Users/91801/Desktop/Insurance Project/models/claim_amount.pkl":
        st.title("💵 Claim Amount")
        feature_1 = abs(st.number_input("Customer Age"))
        feature_2 = abs(st.number_input("Annual Income"))
        feature_3 = abs(st.number_input("Property Age"))
        feature_4 = abs(st.number_input("Claim History"))
        feature_5 = abs(st.number_input("Risk Score"))
        feature_6 = abs(st.number_input("Premium Amount"))
        feature_7 = abs(st.number_input("Fraudulent Claim"))
        feature_8 = abs(st.number_input("Claim Premium Ratio"))
        feature_9 = abs(st.number_input("Gender Male"))
        feature_10 = abs(st.number_input("Health Policy"))
        feature_11 = abs(st.number_input("Life policy"))
        feature_12 = abs(st.number_input("Property policy"))
        input_data = [[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11, feature_12]]

    elif st.session_state.selected_model == "C:/Users/91801/Desktop/Insurance Project/models/customer_segmentation.pkl":
        st.title("👥 Customer Semgmentation")
        feature_1 = abs(st.number_input("Customer Age"))
        feature_2 = abs(st.number_input("Location"))
        feature_3 = abs(st.number_input("Income Level"))
        feature_4 = abs(st.number_input("Coverage Amount"))
        feature_5 = abs(st.number_input("Premium Amount"))
        feature_6 = abs(st.number_input("Policy Upgrades"))
        feature_7 = abs(st.number_input("Number Of Policies"))
        feature_8 = abs(st.number_input("Gender Male"))
        feature_9 = abs(st.number_input("Occupation Doctor"))
        feature_10 = abs(st.number_input("Occupation Engineer"))
        feature_11 = abs(st.number_input("Occupation Entrepreneur"))
        feature_12 = abs(st.number_input("Occupation Lawyer"))
        feature_13 = abs(st.number_input("Occupation Manager"))
        feature_14 = abs(st.number_input("Occupation Nurse"))
        feature_15 = abs(st.number_input("Occupation Salesperson"))
        feature_16 = abs(st.number_input("Occupation Teacher"))
        input_data = [[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11, feature_12, feature_13, feature_14, feature_15, feature_16]]

    elif st.session_state.selected_model == "C:/Users/91801/Desktop/Insurance Project/models/fraud_detection.pkl":
        st.title("🚨 Fraud Detection")
        feature_1 = abs(st.number_input("Claim Amount"))
        feature_2 = abs(st.number_input("Suspicious Flag"))
        feature_3 = abs(st.number_input("Claim Medical"))
        feature_4 = abs(st.number_input("Claim Vehicle"))
        input_data = [[feature_1, feature_2, feature_3, feature_4]]

    elif st.session_state.selected_model == "C:/Users/91801/Desktop/Insurance Project/models/insurance_translate.pkl":
        st.title("🌐 Multilingual File Translator")
        uploaded_file = st.file_uploader("📁 Upload your file", type=["txt", "docx", "pdf"])
        src_lang = st.selectbox("🔤 From Language", ["en", "ta", "hi", "fr", "de", "es"])
        dest_lang = st.selectbox("🔠 To Language", ["en", "ta", "hi", "fr", "de", "es"])

        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
                tmp.write(uploaded_file.read())
                temp_path = tmp.name

        if st.button("Translate"):
            try:
                translated_text = extract_text_and_translate(temp_path, src_lang, dest_lang)
                st.success("✅ Translation Complete")
                st.text_area("📄 Translated Output", translated_text, height=300)
            except Exception as e:
                st.error(f"❌ Error: {e}")

    elif st.session_state.selected_model == "C:/Users/91801/Desktop/Insurance Project/models/sentiment_analysis.pkl":
        st.title("💭 Sentiment Analysis")
        user_input = st.text_area("Enter text to analyze", height=200)

        if st.button("Analyze Sentiment"):
            result = sentiment_analysis(user_input)
            st.markdown(f"### 🗣️ Sentiment - **{result}**")
            if result == "Positive":
                st.success("😊 Positive sentiment detected!")
            elif result == "Negative":
                st.error("😞 Negative sentiment detected!")
            else:
                st.info("😐 Neutral sentiment detected.")

    elif st.session_state.selected_model == "C:/Users/91801/Desktop/Insurance Project/models/text_summarization.pkl":
        st.title("📝 Text Summarization")
        user_input = st.text_area("Enter the text to summarize", height=250)

        if st.button("Summarize"):
            if user_input.strip():
                with st.spinner("Generating summary..."):
                    result = summarize_text(user_input)
                st.success("✅ Summary Generated")
                st.text_area("Output", result, height=200)
            else:
                st.warning("⚠️ Please enter some text to summarize.")

    elif st.session_state.selected_model == "C:/Users/91801/Desktop/Insurance Project/models/chatbot_model.pkl":
        st.title("🌀 Insurance ChatBot")
        query = st.text_input("Ask your question:")

        if st.button("Answer"):
            with st.spinner("Generating Answer..."):
                result = get_best_answer(query)
            st.success(f"**Answer:** {result}")

    # Prediction button
    if input_data:
        if st.button("Predict"):
            input_array = np.array(input_data)
            prediction = model.predict(input_array)[0]
            st.markdown(f"### Prediction : **{prediction}**")



# ⚠️ Warning
# 🟢 Low Risk
# 🟡 Medium Risk
# 🔴 High Risk
# 🧠 Decision

        # prediction_labels = {
        #     "ckd": "Chronic Kidney Disease ⚠️",
        #     "notckd": "No Kidney Disease 😊",
        #     1 : "Liver Disease Detected ⚠️",
        #     0 : "No Liver Disease 😊",
        #     2 : "Parkinson's Disease ⚠️",
        #     3 : "No Parkinson's Disease 😊"}

        # result = prediction_labels.get(prediction)