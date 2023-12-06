import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from datetime import datetime, timedelta
import requests
import os

#image = Image.open('images/logo-no-background.png')
#st.image(image)
st.title(':blue[Lendy]')

selected = option_menu(
    menu_title = None,
    options = ["Home", "Apply", "About us"],
    icons = ["house-fill", "file-earmark-check-fill", "people"],
    default_index=0,
    orientation="horizontal"
)

if selected == "Home":
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(':blue[Access Loans Instantly]')
        st.caption(body="Welcome to Lendy - Your Gateway to Financial Freedom! \n\nAt Lendy, we understand that life is full of unexpected twists and turns, and sometimes you need a helping hand to navigate through. That's why we've created a seamless and user-friendly platform to connect you with the financial solutions you need. Say goodbye to lengthy processes and hello to quick and easy access to loans!")
        st.caption(unsafe_allow_html=True,
                body="<b>Apply by filling our loan application forms and get access to loans now!!!</b>")

    with col2:
        path = os.path.dirname(__file__)
        my_image = path+'/loans.png'
        image = Image.open(my_image)
        st.image(image)

elif selected == "Apply":
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(':blue[Personal information]')
        name = st.text_input('Full Name', placeholder="Enter full name...")
        email = st.text_input('Email Address', placeholder="example@gmail.com")
        gender = st.radio("Gender",["Male", "Female"])
        education = st.selectbox("Education", ['Graduate', 'Not Graduate'],index=None)
        self_employed = st.selectbox("Self Employed", ['No', 'Yes'],index=None)
        married = st.radio("Married",["No", "Yes"])
        dependents = st.selectbox("Number of Dependents",['0', '1', '2', '3+'])
        property_area = st.selectbox("Property Area", ['Urban', 'Rural', 'Semiurban'])

    with col2:
        st.subheader(':blue[Loan information]')

        App_income = st.number_input("Your Monthly Income", value=None, placeholder="Enter amount...")
        coapp_income = st.number_input("Co-applicants Monthly Income", value=None, placeholder="Enter amount...")
        loan_amount = st.number_input("Loan Amount", value=None, placeholder="Enter amount...")
        
        today = datetime.now()
        one_year = today + timedelta(days = 480)
        how_long = st.date_input("When can you pay back this loan?", format='DD/MM/YYYY', min_value=today, max_value=one_year)
                                 #on_change = st.write("You are expected to pay back in {} days".format((today - how_long).days)))
        credit_history = st.radio("Credit History",["1", "0"],captions=["You have taken a loan before","You haven't taken a loan before"])
    
    # =============Submit Handler===============
    def name_input():
        """Check name input"""
        if name.isdigit() == True or name == "":
            st.toast('Enter a valid Name', icon='❌')
            return 'No'
        else:
            return 'Yes'
    def email_input():
        """Check email input"""
        if email.isdigit() == True or email == "":
            st.toast('Enter a valid Email', icon='❌')
            return 'No'
        else:
            return 'Yes'
    def number_inputs():
        if App_income == None or coapp_income == None or loan_amount == None:
            st.toast('Enter an amount', icon='❌')
            return 'No'
        else:
            return 'Yes'
        
    days = (how_long - today.date()).days
    loan_amount_term = 0.0
    if days <= 480 and days > 360:
        loan_amount_term = 480.0
    elif days <= 360 and days > 300:
        loan_amount_term = 360.0
    elif days <= 300 and days > 240:
        loan_amount_term = 300.0
    elif days <= 240 and days > 180:
        loan_amount_term = 240.0
    elif days <= 180 and days > 120:
        loan_amount_term = 180.0
    elif days <= 120 and days > 84:
        loan_amount_term = 120.0
    elif days <= 84 and days > 60:
        loan_amount_term = 84.0
    elif days <= 60 and days > 36:
        loan_amount_term = 60.0
    elif days <= 36 and days > 12:
        loan_amount_term = 36.0
    elif days <= 12 and days > 0:
        loan_amount_term = 12.0
    else:
        pass

    _col1, _col2, _col3 = st.columns(3)
    
    with _col2:
        if st.button("Apply", use_container_width=True):
            
            check_name = name_input()
            check_email = email_input()
            check_number = number_inputs()

            if check_name == 'No' or check_email == 'No' or check_number == 'No':
                pass
            else:
                url = 'https://j8cb2dmnjd.execute-api.eu-north-1.amazonaws.com/stream' # Api URL
                myobj = [{
                        "Name":name,
                        "Email":email,
                        "Gender":gender,
                        "Married":married,
                        "Dependents":dependents,
                        "Education":education,
                        "Self_Employed":self_employed,
                        "ApplicantIncome":str(App_income),
                        "CoapplicantIncome":str(coapp_income),
                        "LoanAmount":str(loan_amount),
                        "Loan_Amount_Term":str(loan_amount_term),
                        "Credit_History":credit_history,
                        "Property_Area":property_area
                        }]
                try:
                    requests.post(url, json = myobj) # Post Request
                    st.toast('Application Submitted', icon='✅')
                except Exception as e:
                    st.toast('Error Sending Request {}'.format(e), icon='❌')

if selected == "About us":
    st.subheader(':blue[Why Choose Lendy?]')
    st.caption(unsafe_allow_html=True,body="<b>Instant Access to Loans:</b>\n\nNo more waiting around! At Lendy, we offer instant access to loans. Simply fill out our easy-to-use loan application forms, and you could have the funds you need in no time. We value your time, and our streamlined process ensures a hassle-free experience.")
    st.caption(unsafe_allow_html=True,body="<b>Tailored Solutions for You:</b>\n\nWe believe that financial solutions should be as unique as you are. Our team at Lendy works tirelessly to understand your needs and provide personalized loan options that fit your lifestyle. Whether it's for a home renovation, education, or unexpected expenses, we've got you covered.")
    st.caption(unsafe_allow_html=True,body="<b>Transparent and Fair:</b>\n\nWe believe in transparency every step of the way. No hidden fees or confusing terms. At Lendy, we are committed to providing clear and fair loan options, so you can make informed decisions about your financial future.")
    st.caption(unsafe_allow_html=True,body="<b>Secure and Confidential:</b>\n\nYour security is our top priority. Rest easy knowing that your information is handled with the utmost confidentiality and security. Lendy employs industry-leading measures to protect your data, giving you peace of mind throughout the loan process.")