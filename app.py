import streamlit as st
import pandas as pd
import pickle
import time
import streamlit.components.v1 as components 

st.set_page_config(
    page_title="Loan Default Predictor",
    page_icon="💸",
    layout="wide" 
)

@st.cache_resource
def load_model():
    try:
        with open('loan_default_pipeline.pkl', 'rb') as f:
            pipeline = pickle.load(f)
        return pipeline
    except FileNotFoundError:
        st.error("Model file 'loan_default_pipeline.pkl' not found. Please make sure it's in the same directory.")
        return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

pipeline = load_model()

options_education = ['Bachelor\'s', 'Master\'s', 'High School', 'PhD', 'Some College', 'Associate']
options_employment = ['Full-time', 'Unemployed', 'Part-time', 'Self-employed', 'Student']
options_marital = ['Divorced', 'Married', 'Single']
options_mortgage = ['Yes', 'No']
options_dependents = ['Yes', 'No']
options_purpose = ['Other', 'Auto', 'Business', 'Home', 'Education', 'Personal']
options_cosigner = ['Yes', 'No']

# PART 1: THE "WHAT-IF" PREDICTOR

st.title("💸 Loan Default Risk Predictor")
st.markdown("Use the sliders and dropdowns to predict a new applicant's default risk.")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Applicant Info")
    age = st.slider("Age", 18, 75, 30)
    income = st.number_input("Annual Income ($)", min_value=10000, max_value=1000000, value=50000, step=1000)
    months_employed = st.slider("Months Employed", 0, 480, 24)
    education = st.selectbox("Education Level", options=options_education)
    employment_type = st.selectbox("Employment Type", options=options_employment)
    marital_status = st.selectbox("Marital Status", options=options_marital)

with col2:
    st.header("Loan Details")
    loan_amount = st.number_input("Loan Amount ($)", min_value=500, max_value=100000, value=10000, step=500)
    interest_rate = st.slider("Interest Rate (%)", 1.0, 30.0, 10.0, 0.1)
    loan_term = st.slider("Loan Term (Months)", 12, 72, 36)
    loan_purpose = st.selectbox("Loan Purpose", options=options_purpose)
    has_cosigner = st.selectbox("Has Co-Signer?", options=options_cosigner)

with col3:
    st.header("Financial Health")
    credit_score = st.slider("Credit Score", 300, 850, 650)
    num_credit_lines = st.number_input("Number of Credit Lines", min_value=0, max_value=50, value=5)
    dti_ratio = st.slider("Debt-to-Income (DTI) Ratio", 0.0, 1.0, 0.3, 0.01)
    has_mortgage = st.selectbox("Has Mortgage?", options=options_mortgage)
    has_dependents = st.selectbox("Has Dependents?", options=options_dependents)

st.markdown("---")
predict_button = st.button("🔮 Predict Default Risk", type="primary")

if predict_button and pipeline is not None:
    input_data = {
        'Age': age, 'Income': income, 'LoanAmount': loan_amount,
        'CreditScore': credit_score, 'MonthsEmployed': months_employed,
        'NumCreditLines': num_credit_lines, 'InterestRate': interest_rate,
        'LoanTerm': loan_term, 'DTIRatio': dti_ratio,
        'Education': education, 'EmploymentType': employment_type,
        'MaritalStatus': marital_status, 'HasMortgage': has_mortgage,
        'HasDependents': has_dependents, 'LoanPurpose': loan_purpose,
        'HasCoSigner': has_cosigner
    }
    
    input_df = pd.DataFrame([input_data])

    with st.spinner('Analyzing risk...'):
        try:
            prediction = pipeline.predict(input_df)[0]
            probability = pipeline.predict_proba(input_df)[0]
            prob_of_default = probability[1] * 100
            
            if prediction == 0:
                st.success(f"**Low Risk (Likely to Repay)**")
                st.metric(label="Probability of Default", value=f"{prob_of_default:.2f}%")
            else:
                st.error(f"**High Risk (Likely to Default)**")
                st.metric(label="Probability of Default", value=f"{prob_of_default:.2f}%")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

elif predict_button and pipeline is None:
    st.error("Model is not loaded. Cannot make prediction.")

# PART 2: THE EMBEDDED POWER BI DASHBOARD

st.markdown("---")
st.header("Project Power BI Dashboard")
st.markdown("This is the existing interactive dashboard showing historical loan data.")

power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiNzg1YTk2N2UtZmQ5Ni00M2Y0LTg1YWQtNDA4YWMyMTZlMWY1IiwidCI6ImVjMTQyODJlLTkzZjAtNGI1Mi1hNzkwLWZkOGMwN2Y2MGQ1OCJ9"

try:
    components.iframe(power_bi_url, height=700, scrolling=True)
except Exception as e:
    st.error(f"Could not load Power BI dashboard. Please check the URL. Error: {e}")