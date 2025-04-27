## Insurance AI Project

## Project Overview
This project aims to develop a machine learning model & deep learning to predict insurance related outcomes, utilizing a variety of techniques such as classification, regression, and NLP. The project is designed to help in decision making processes for insurance companies by providing predictions based on historical data.

The model is build using a combination of Exploratry data Analysis, data preprocessing techniques, machine learning algorithms, and model evaluation metrics. The final model is deployed with a user friendly interface using Streamlit for easy interaction.


## Dataset Used
- **Source**: [Dataset Source like Kaggle, OpenML, creating synthetic Data, etc.]
- **Description**: This dataset contains information about customer details, claim amounts, Policy Type and other insurance related variables.
- **Preprocessing Details**:
  - Handling missing values using imputation `fillna()` or `dropna()`.
  - Categorical feature encoding using `LabelEncoder`.
  - Feature scaling using `StandardScaler`.
  - Data splitting into training and testing sets `train_test_split`.


## Machine Learning Techniques Applied
The following machine learning techniques applied in this project:
**Classification**:
  - `RandomForestClassifier`
  - `LogisticRegression`
**Regression**:
  - `LinearRegression`
  - `Ridge`
  - `Lasso`
  - `ElasticNet`
**Clustering**:
  - `KMeans`
**Natural Language Processing (NLP)**:
  - Sentiment analysis using `TextBlob` for text classification.
  - Text Translation using `googletrans` for translating text between languages.
**Model Evaluation**:
  - Metrics such as `accuracy_score`, `f1_score`, `precision_score`, `recall_score`, `confusion_matrix` for classification tasks.
  - Metrics such as `mean_squared_error`, `mean_absolute_error`, `Root_mean_absolute_error` `r2_score` for regression tasks.
  - Metrics such as `silhouette_score` for unsupervised learning.

## Classification Models
Used for Risk Classification and Fraud Detection, classifying customers.
## Regression Models
Applied for Claim Amount Prediction, Insurance claim Amount Estimation, and continuous outcome forecasting.
## Clustering (Unsupervised Learning)
Used in Customer Segmentation to group policyholders for tailored marketing and plan recommendations.
## NLP Techniques
Sentiment Analysis Analyzing customer reviews and complaints. Insurance Document Translation Automatically translating insurance policies.

**Deployment Instructions**:
   - Install dependencies via `pip install -r requirements.txt`.
   - cd `Insurance_AI_Project`.
   - Run the Streamlit app using `streamlit run app.py`.