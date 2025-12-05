import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(
    page_title="Customer Churn Predictor",
    layout="wide"
)
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Input"
if 'prediction_data' not in st.session_state:
    st.session_state.prediction_data = None
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'validation_state' not in st.session_state:
    st.session_state.validation_state = {
        'customer_data_valid': False
    }
def switch_to_tab(tab_name):
    st.session_state.current_tab = tab_name

def back_to_input():
    switch_to_tab("Input")

def display_header():
    try:
        col1, col2, col3 = st.columns([1, 10, 1])
        with col1:
            try:
                logo = Image.open("image-removebg-preview.png")
                st.image(logo, width=60)  # Smaller logo
            except Exception as e:
                pass   
        with col2:
            st.markdown("""
                <h1 style="text-align: center; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; line-height: 1; color: #F79E1B;">Customer Churn Prediction</h1>
            """, unsafe_allow_html=True)
        with col3:
            pass
    except Exception as e:
        st.title("Customer Churn Prediction")

def input_tab():
    display_header()
    st.markdown("""
    <p style="font-size: 14px;">Fill in the customer details below and click 'Predict Churn' to get a prediction.</p>
    """, unsafe_allow_html=True)
    with st.form("customer_data_form", clear_on_submit=False):
        st.subheader("Customer Information")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Personal Details")
            age = st.number_input("Age", min_value=18, max_value=100, value=None, placeholder="Enter age...")
            married_col1, married_col2 = st.columns(2)
            with married_col1:
                st.write("Married")
            with married_col2:
                married = st.radio("Married", ["Yes", "No"], index=None, horizontal=True, label_visibility="collapsed")
            dependents_col1, dependents_col2 = st.columns(2)
            with dependents_col1:
                st.write("Has Dependents")
            with dependents_col2:
                dependents = st.radio("Has Dependents", ["Yes", "No"], index=None, horizontal=True, label_visibility="collapsed")
            st.markdown("##### Account Details")
            tenure = st.number_input("Tenure in Months", min_value=1, max_value=100, value=None, placeholder="Enter tenure...")
            contract = st.selectbox("Contract Type", ["Month-to-Month", "One Year", "Two Year"], index=None)
            payment_method = st.selectbox("Payment Method", [
                "Electronic Check", "Mailed Check", "Bank Transfer (automatic)", "Credit Card (automatic)"
            ], index=None)
            offer = st.selectbox("Current Offer", ["No Offer", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"], index=None)
        with col2:
            st.markdown("##### Services")
            phone_col1, phone_col2 = st.columns(2)
            with phone_col1:
                st.write("Phone Service")
            with phone_col2:
                phone_service = st.radio("Phone Service", ["Yes", "No"], index=None, horizontal=True, label_visibility="collapsed")
                
            internet_type = st.selectbox("Internet Type", ["DSL", "Fiber Optic", "Cable", "None"], index=None)
            avg_monthly_gb = st.number_input(
                "Avg Monthly GB Download", 
                min_value=0.0, 
                max_value=500.0, 
                value=None,
                placeholder="Enter GB..."
            )
            st.markdown("##### Financial Information")
            monthly_charge = st.number_input("Monthly Charge ($)", min_value=0.0, max_value=200.0, value=None, placeholder="Enter amount...")
            total_revenue = st.number_input("Total Revenue ($)", min_value=0.0, max_value=10000.0, value=None, placeholder="Enter amount...")
            cltv = st.number_input("CLTV ($)", min_value=0.0, max_value=10000.0, value=None, placeholder="Enter amount...")
            st.markdown("##### Satisfaction")
            satisfaction_score = st.slider("Satisfaction Score", 1, 5, value=3)
        submitted = st.form_submit_button("Predict Churn", type="primary", use_container_width=True)
        
        if submitted:
            required_fields = [
                ('age', age, "Please enter the customer's age"),
                ('married', married, "Please select marital status"),
                ('dependents', dependents, "Please select if customer has dependents"),
                ('tenure', tenure, "Please enter tenure in months"),
                ('contract', contract, "Please select a contract type"),
                ('payment_method', payment_method, "Please select a payment method"),
                ('offer', offer, "Please select current offer"),
                ('phone_service', phone_service, "Please select phone service status"),
                ('internet_type', internet_type, "Please select internet type"),
                ('avg_monthly_gb', avg_monthly_gb, "Please enter average monthly GB download"),
                ('monthly_charge', monthly_charge, "Please enter monthly charge"),
                ('total_revenue', total_revenue, "Please enter total revenue"),
                ('cltv', cltv, "Please enter customer lifetime value")
            ]
            
            validation_errors = []
            for field_name, field_value, error_msg in required_fields:
                if field_value is None:
                    validation_errors.append(error_msg)
            
            if validation_errors:
                for error in validation_errors:
                    st.warning(error)
                st.session_state.validation_state['customer_data_valid'] = False
            else:
                st.session_state.validation_state['customer_data_valid'] = True
                
                # Prepare data for prediction
                under_30 = "Yes" if age < 30 else "No"
                senior_citizen = "Yes" if age >= 65 else "No"
                
                # Create payload for API call
                payload = {
                    "Tenure_in_Months": tenure,
                    "Offer": offer,
                    "Phone_Service": phone_service,
                    "Avg_Monthly_Long_Distance_Charges": 0.0,  # Defaulting to 0 as this field was removed
                    "Multiple_Lines": "No",  # Defaulting to "No" as this field was removed
                    "Internet_Type": internet_type,
                    "Avg_Monthly_GB_Download": avg_monthly_gb if avg_monthly_gb is not None else 0.0,  # Handle None value
                    "Online_Security": "No",  # Defaulted
                    "Online_Backup": "No",  # Defaulted
                    "Device_Protection_Plan": "No",  # Defaulted
                    "Premium_Tech_Support": "No",  # Defaulted
                    "Streaming_TV": "No",  # Defaulted
                    "Streaming_Movies": "No",  # Defaulted
                    "Streaming_Music": "No",  # Defaulted
                    "Unlimited_Data": "No",  # Defaulted
                    "Contract": contract,
                    "Paperless_Billing": "No",  # Defaulted
                    "Payment_Method": payment_method,
                    "Monthly_Charge": monthly_charge,
                    "Total_Charges": monthly_charge * tenure,  # Calculate total charges
                    "Total_Refunds": 0.0,  # Defaulted
                    "Total_Extra_Data_Charges": 0.0,  # Defaulted
                    "Total_Long_Distance_Charges": 0.0,  # Defaulted
                    "Total_Revenue": total_revenue,
                    "Satisfaction_Score": satisfaction_score,
                    "CLTV": cltv,
                    "Gender": "Male",  # Defaulted as this field was removed
                    "Age": age,
                    "Under_30": under_30,
                    "Senior_Citizen": senior_citizen,
                    "Married": married,
                    "Dependents": dependents,
                    "Number_of_Dependents": 0  # Defaulted as this field was removed
                }
                
                try:
                    API_ENDPOINT = "http://127.0.0.1:8000/predict"
                    response = requests.post(API_ENDPOINT, json=payload)
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Generate risk factors, positive factors and recommendations based on the prediction
                        risk_factors = []
                        positive_factors = []
                        recommendations = []
                        
                        # Logic to determine risk factors
                        if contract == "Month-to-Month":
                            risk_factors.append("Short-term contract increases churn risk")
                            recommendations.append("Offer incentives to upgrade to annual contract")
                        
                        if satisfaction_score <= 3:
                            risk_factors.append(f"Low satisfaction score ({satisfaction_score}/5)")
                            recommendations.append("Schedule follow-up call to address concerns")
                        
                        if tenure < 12:
                            risk_factors.append("New customer (less than 1 year)")
                            recommendations.append("Enroll in customer loyalty program")
                        
                        # Logic for positive factors
                        if internet_type == "Fiber Optic":
                            positive_factors.append("High-value internet service")
                        
                        if payment_method in ["Bank Transfer (automatic)", "Credit Card (automatic)"]:
                            positive_factors.append("Using automatic payment method")
                        
                        if tenure > 24:
                            positive_factors.append("Long-term customer (over 2 years)")
                        
                        # Additional recommendations
                        if cltv > 1000 and result["churn_prediction"] == 1:
                            recommendations.append("High-value customer retention: Offer personalized discount")
                        
                        # Default recommendations if none were generated
                        if not recommendations:
                            if result["churn_prediction"] == 1:
                                recommendations.append("Offer promotional discount on current plan")
                                recommendations.append("Conduct satisfaction survey to identify pain points")
                            else:
                                recommendations.append("Offer upsell opportunities for additional services")
                                recommendations.append("Enroll in referral program")
                        
                        # Store the prediction data with generated insights
                        st.session_state.prediction_data = {
                            "prediction": result["churn_prediction"],
                            "churn_probability": result["churn_probability"],
                            "no_churn_probability": result["no_churn_probability"],
                            "risk_factors": risk_factors,
                            "positive_factors": positive_factors,
                            "recommendations": recommendations,
                            "customer_data": {
                                "age": age,
                                "married": married,
                                "dependents": dependents,
                                "tenure": tenure,
                                "contract": contract,
                                "payment_method": payment_method,
                                "offer": offer,
                                "internet_type": internet_type,
                                "monthly_charge": monthly_charge,
                                "satisfaction_score": satisfaction_score
                            }
                        }
                        switch_to_tab("Results")
                        st.experimental_rerun()
                    else:
                        st.error(f"Error from API: {response.text}")
                except Exception as e:
                    st.error(f"Error making prediction: {str(e)}")
                    st.write("Please check if the API is running and accessible.")

# Function to display prediction results
def results_tab():
    display_header()
    
    st.subheader("Churn Prediction Results")
    
    if st.session_state.prediction_data:
        data = st.session_state.prediction_data
        
        # Summary of customer data - more compact
        with st.expander("Customer Details"):
            # Two column layout for all customer details for compactness
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("<p style='font-size:13px; font-weight:bold; margin-bottom:5px;'>Personal & Account</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Age: {data['customer_data']['age']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Married: {data['customer_data']['married']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Dependents: {data['customer_data']['dependents']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Tenure: {data['customer_data']['tenure']} months</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Contract: {data['customer_data']['contract']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Payment: {data['customer_data']['payment_method']}</p>", unsafe_allow_html=True)
            
            with col_right:
                st.markdown("<p style='font-size:13px; font-weight:bold; margin-bottom:5px;'>Service & Satisfaction</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Offer: {data['customer_data']['offer']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Internet: {data['customer_data']['internet_type']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Monthly: ${data['customer_data']['monthly_charge']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:12px; margin:0;'>Satisfaction: {data['customer_data']['satisfaction_score']}/5</p>", unsafe_allow_html=True)
        
        # Prediction results
        col_result1, col_result2 = st.columns(2)
        
        with col_result1:
            st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
            
            if data["prediction"] == 1:  # Churn prediction
                st.error("### Prediction: Customer Will Churn")
                relevant_probability = data["churn_probability"]
                probability_label = "Churn Probability"
                gauge_color = "darkred"
                threshold_value = 50
            else:  # No churn prediction
                st.success("### Prediction: Customer Will Stay")
                relevant_probability = data["no_churn_probability"]
                probability_label = "Stay Probability"
                gauge_color = "green"
                threshold_value = 50
        
        with col_result2:
            gauge = {
                "data": [
                    {
                        "type": "indicator",
                        "mode": "gauge+number",
                        "value": float(relevant_probability * 100),
                        "title": {"text": probability_label, "font": {"size": 14}},
                        "gauge": {
                            "axis": {"range": [0, 100], "tickfont": {"size": 10}},
                            "bar": {"color": gauge_color},
                            "steps": [
                                {"range": [0, 30], "color": "lightgray"},
                                {"range": [30, 70], "color": "lightyellow"},
                                {"range": [70, 100], "color": "lightgreen" if data["prediction"] == 0 else "salmon"}
                            ],
                            "threshold": {
                                "line": {"color": "red", "width": 3},
                                "thickness": 0.75,
                                "value": threshold_value
                            }
                        }
                    }
                ],
                "layout": {"height": 200, "margin": {"t": 30, "b": 0, "l": 20, "r": 20}}
            }
            
            fig = go.Figure(gauge["data"], gauge["layout"])
            st.plotly_chart(fig, use_container_width=True)

        # Side-by-side Analysis and Recommended Actions - more compact
        col_analysis, col_recommendations = st.columns(2)

        with col_analysis:
            st.markdown("<h2 style='font-size:25px; margin-bottom:10px; font-weight:bold;'>Analysis</h2>", unsafe_allow_html=True)
            if data["risk_factors"]:
                st.markdown("<p style='font-size:18px; font-weight:bold; margin-bottom:5px;'>Risk Factors:</p>", unsafe_allow_html=True)
                for factor in data["risk_factors"]:
                    st.markdown(f"<p style='font-size:16px; margin:0 0 4px 15px;'>• {factor}</p>", unsafe_allow_html=True)
            if data["positive_factors"]:
                st.markdown("<p style='font-size:18px; font-weight:bold; margin-bottom:5px; margin-top:10px;'>Positive Factors:</p>", unsafe_allow_html=True)
                for factor in data["positive_factors"]:
                    st.markdown(f"<p style='font-size:16px; margin:0 0 4px 15px;'>• {factor}</p>", unsafe_allow_html=True)

        with col_recommendations:
            st.markdown("<h2 style='font-size:25px; margin-bottom:10px; font-weight:bold;'>Recommended Actions</h2>", unsafe_allow_html=True)
            if data["recommendations"]:
                for rec in data["recommendations"]:
                    st.markdown(f"<p style='font-size:16px; margin:0 0 4px 15px;'>• {rec}</p>", unsafe_allow_html=True)

        # Back button - smaller and more compact
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        col_back1, col_back2, col_back3 = st.columns([2, 3, 2])
        with col_back2:
            if st.button("Predict Another Customer", type="secondary", use_container_width=True):
                # Reset validation state when starting fresh
                st.session_state.validation_state = {
                    'customer_data_valid': False
                }
                back_to_input()

# Add custom CSS
    st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
            max-width: 1000px;
        }
        h1 {
            color: #F79E1B;
            text-align: center;
            font-size: 24px;
            margin-bottom: 0;
        }
        h3 {
            color: #3F3E3E;
            font-size: 18px;
        }
        h5 {
            font-size: 15px;
            margin-bottom: 5px;
            margin-top: 10px;
        }
        .stButton>button {
            width: 100%;
            height: 2.5em;
            font-size: 14px;
        }
        /* Make input fields more compact */
        .stNumberInput div[data-baseweb="input"] {
            width: 100%;
        }
        .stRadio [data-testid="stRadio"] {
            margin-bottom: 0;
            padding-bottom: 0;
        }
        .stRadio > div {
            margin-bottom: 0;
            padding-bottom: 0;
        }
        /* Reduce spacing for all form elements */
        div[data-testid="stVerticalBlock"] > div {
            padding-top: 0.25rem !important;
            padding-bottom: 0.25rem !important;
        }
        .stSelectbox {
            margin-bottom: 0;
            padding-bottom: 0;
        }
        /* Reduce space around columns */
        [data-testid="column"] {
            padding: 0.5rem !important;
        }
        /* Reduce space between sections */
        p {
            margin-bottom: 0.5rem;
        }
        /* For proper logo alignment */
        [data-testid="column"]:first-child {
            text-align: left;
        }
        /* Style for validation notifications */
        .stSuccess {
            background-color: #D4EDDA;
            color: #155724;
            padding: 5px;
            border-radius: 5px;
            margin-bottom: 5px;
        }
        .stWarning {
            background-color: #FFF3CD;
            color: #856404;
            padding: 5px;
            border-radius: 5px;
            margin-bottom: 5px;
        }
        .stError {
            background-color: #F8D7DA;
            color: #721C24;
            padding: 5px;
            border-radius: 5px;
            margin-bottom: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

# Display the appropriate tab based on session state
if st.session_state.current_tab == "Input":
    input_tab()
elif st.session_state.current_tab == "Results":
    results_tab()