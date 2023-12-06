import json
import binascii
import boto3

from email.message import EmailMessage
import ssl
import smtplib

import joblib
import pandas as pd

label_mappings = {'Gender': ['Male', 'Female'],
                'Married': ['No', 'Yes'],
                'Dependents': ['0', '1', '2', '3+'],
                'Education': ['Graduate', 'Not Graduate'],
                'Self_Employed': ['No', 'Yes'],
                'Property_Area': ['Urban', 'Rural', 'Semiurban'],
                'Loan_Status': ['Y', 'N']
                }

def lambda_handler(event, context):
    # Handle Event
    for record in event['Records']:
        decoded_data = binascii.a2b_base64(record['kinesis']['data'])
        data = json.loads(decoded_data)

        # Pop name and email fields from the dictionary 
        name = data['Name']
        email = data['Email']
        data.pop('Name', None)
        data.pop("Email", None)

        # Convert related fields from strings to floats
        data.update(
            {'ApplicantIncome': float(data['ApplicantIncome']),
            'CoapplicantIncome': float(data['CoapplicantIncome']),
            'LoanAmount': float(data['LoanAmount']),
            'Loan_Amount_Term': float(data['Loan_Amount_Term']),
            'Credit_History': float(data['Credit_History'])
            }
        )

        # Create a list based on positional values in dict2
        values = [label_mappings[key].index(data[key]) if key in label_mappings else data[key] for key in data]
        column = ["Gender", "Married", "Dependents", "Education", "Self_Employed", "ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area"]
        
        # Load files
        # Load model and 
        try:
            new_rf = joblib.load("model.joblib")
            new_scaler = joblib.load("scaler.joblib")
        except FileNotFoundError as e:
            print("Model file not found")

        df = pd.DataFrame([values], columns=column)

        # Preprocessing
        data_normalized = new_scaler.fit_transform(df)

        rf_preds = new_rf.predict(data_normalized)

        if rf_preds[0] == 0:
            predicted = "Eligible"
        else:
            predicted = "Not Eligible"

        try:
            #===== Message to Stakeholder =======
            message = "Dear Stakeholder, \n\nA new application with data: \n Name: {}, Gender: {}, Married: {}, Dependents: {}, Education: {}, Self_Employed: {}, ApplicantIncome: {}, CoapplicantIncome: {}, LoanAmount: {}, Loan_Amount_Term: {}, Credit_History: {}, Property_Area: {}\n has been processed. \n\There are {} for this loan as predicted by the model, Kindly look further into their application."\
            .format(name,data['Gender'],data['Married'],data['Dependents'],data['Education'],data['Self_Employed'],data['ApplicantIncome'],data['CoapplicantIncome'],data['LoanAmount'],data['Loan_Amount_Term'],data['Credit_History'],data['Property_Area'],predicted)
            subject = "Application {} Notification".format(predicted)
            SNSResult = send_sns(message, subject)
            if SNSResult:
                print("Notification Sent..")
                
            #====== Message to Applicant =======
            email_sender = 'nidaabraham80@gmail.com'
            email_password = 'fsqs bwsd crae zjyh'

            if predicted == "Not Eligible":
                message2 = "Unfortunately you are Not Eligible for the loan of {} at this time. We also cannot give more information.".format(str(data["LoanAmount"]))
            else:
                message2 = "Congratulations you are Eligible for the loan of {}.".format(str(data["LoanAmount"]))

            email_reciever = email
            subject = "Loan Application Notification"
            body = """Important Update on your loan application: {}.\n {} \nKindly reach out to support if you have any queries, Thank you.
            """.format(name, message2)

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_reciever
            em['subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender,email_reciever,em.as_string())

        except Exception as e:
            return "Email Error: {}".format(e)
        
    
topic_arn = "arn:aws:sns:eu-north-1:424183295928:datastream_sns"
def send_sns(message, subject):
    try:
        client = boto3.client("sns")
        result = client.publish(TopicArn=topic_arn, Message=message, Subject=subject)
        if result['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(result)
            print("Notification send successfully..!!!")
            return True
    except Exception as e:
        print("Error occured while publish notifications and error is : ", e)
        return True