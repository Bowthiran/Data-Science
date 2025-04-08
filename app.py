import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🕵️‍♂️ Insurance Fraud Detection App")

# Upload CSV
uploaded_file = st.file_uploader("Upload Insurance Claim CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Uploaded Data")
    st.dataframe(df.head())

    # Preprocessing
    df['Suspicious_Flags'] = df['Suspicious_Flags'].astype(str)
    df['Fraud_Label'] = df['Fraud_Label'].astype(str)
    df['Claim_Type'] = df['Claim_Type'].astype(str)

    ### Association Rule Mining
    arm_df = df[['Claim_Type', 'Suspicious_Flags', 'Fraud_Label']]
    encoded_df = pd.get_dummies(arm_df).applymap(lambda x: 1 if x > 0 else 0)
    frequent_items = apriori(encoded_df, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_items, metric='confidence', min_threshold=0.5)
    fraud_rules = rules[rules['consequents'].astype(str).str.contains('Fraud_Label_1')]

    st.subheader("📌 Association Rules Related to Fraud")
    st.dataframe(fraud_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

    ### Anomaly Detection
    iso = IsolationForest(contamination=0.05, random_state=42)
    df['Anomaly'] = iso.fit_predict(df[['Claim_Amount']])
    df['Anomaly'] = df['Anomaly'].apply(lambda x: 1 if x == -1 else 0)

    ### Machine Learning Model
    df['Suspicious_Flags'] = df['Suspicious_Flags'].map({'True': 1, 'False': 0})
    df = pd.get_dummies(df, columns=['Claim_Type'])
    df['Fraud_Label'] = df['Fraud_Label'].astype(int)

    features = ['Claim_Amount', 'Suspicious_Flags', 'Anomaly'] + \
            [col for col in df.columns if col.startswith('Claim_Type_')]

    X = df[features]
    y = df['Fraud_Label']

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)

    df['ML_Prediction'] = rf.predict(X)

    # Final Ensemble
    df['Final_Prediction'] = ((df['ML_Prediction'] == 1) | (df['Anomaly'] == 1) | (df['Suspicious_Flags'] == 1)).astype(int)

    st.subheader("✅ Final Predictions")
    st.dataframe(df[['Claim_ID', 'Claim_Amount', 'Suspicious_Flags', 'Anomaly', 'Final_Prediction']].head())

    # Download option
    st.download_button("⬇️ Download Results as CSV", df.to_csv(index=False), file_name="fraud_predictions.csv")

    # Feature Importance
    st.subheader("📈 Feature Importance (Random Forest)")
    importances = rf.feature_importances_
    feat_df = pd.DataFrame({"Feature": features, "Importance": importances})
    feat_df = feat_df.sort_values(by="Importance", ascending=False)

    fig, ax = plt.subplots()
    sns.barplot(x="Importance", y="Feature", data=feat_df.head(10), ax=ax)
    st.pyplot(fig)
    
    st.subheader("📉 Final Prediction Distribution")
    fraud_count = df['Final_Prediction'].value_counts().rename({0: 'Legit', 1: 'Fraud'})

    fig2, ax2 = plt.subplots()
    fraud_count.plot.pie(autopct='%1.1f%%', labels=fraud_count.index, colors=["lightgreen", "tomato"], ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)
