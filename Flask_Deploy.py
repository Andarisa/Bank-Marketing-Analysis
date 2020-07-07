from flask import Flask, render_template, url_for, request
import numpy as np
import pandas as pd
import joblib
import mysql.connector as mc


db=mc.connect(host="localhost",
          port=3306,
          user="root",
          passwd="andarisa",
          database="BankCustomer")


cs=db.cursor()

# cs.execute("create database BankCustomer")


# cs.execute("CREATE TABLE customer(job VARCHAR(100), marital_status VARCHAR(100), education VARCHAR(100), def VARCHAR(100), balance VARCHAR(100), housing_loan VARCHAR(100),personal_loan VARCHAR(100), contact VARCHAR(100),date VARCHAR(100), month VARCHAR(100), duration VARCHAR(100), campaign VARCHAR(100), previous VARCHAR(100), agegroup VARCHAR(100), pdays VARCHAR(100), deposit VARCHAR(100))")

# cs.execute("describe customer")

# print(cs.fetchall())




app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Final_Home.html')

@app.route('/result',methods=['POST','GET'])
def result():
    if request.method == 'POST':
        input = request.form

        # Job
        Job= int(input['job'])
        job_list = {0: 'admin', 1:'blue-collar' , 2: 'entrepreneur' , 3: 'housemaid' , 4: 'management', 5: 'retired', 6: 'self-employed',
        7: 'services', 8: 'student', 9: 'technician', 10: 'unemployed'}
        job_category = job_list[Job]        


        # Marital
        Marital = int(input['marital'])
        mar_list = {0: 'divorced', 1:'married', 2:'single'}
        mar_category = mar_list[Marital]


        # Education
        Education = int(input['education'])
        edu_list = {0: 'primary', 1:'secondary', 2:'tertiary'}
        edu_category = edu_list[Education]


        # Default
        Default = int(input['default'])
        dft_list = {0: 'no', 1:'yes'}
        dft_category = dft_list[Default]


        # Balance
        Balance = int(input['balance'])
        balance_val = str(Balance)

        # Housing
        Housing = int(input['housing'])
        hos_list = {0: 'no', 1:'yes'}
        hos_category = hos_list[Housing]


        # Loan
        Loan = int(input['loan'])
        loan_list = {0: 'no', 1:'yes'}
        loan_category = loan_list[Loan]

        # Contact
        Contact = int(input['contact'])
        cnt_list = {0: 'cellular', 1:'telephone'}
        cnt_category = cnt_list[Contact]

        # Day
        Day = int(input['day'])
        day_val = str(Day)

        # Month
        Month= int(input['month'])
        mon_list = {0: 'jan', 1:'feb' , 2: 'mar' , 3: 'apr' , 4: 'may', 5: 'jun', 6: 'jul',
        7: 'aug', 8: 'sep', 9: 'oct', 10: 'nov', 11: 'dec'}
        mon_category = mon_list[Month]   

        # Duration
        Duration = int(input['duration'])
        dur_val = str(Duration)
        
        # Campaign
        Campaign = int(input['campaign'])
        camp_val = str(Campaign)

        # Previous
        Previous = int(input['previous'])
        prev_val = str(Previous)        
        

        # Age Group
        Age = int(input['age'])
        age_list = {0: '17-24', 1:'25-34' , 2: '35-44' , 3: '45-54' , 4: '55-64', 5: '65+'}
        age_category = age_list[Age]

        # Pdays Group
        Pdays = int(input['pdays'])
        pdays_list = {0: '1 to 143 days', 1:'144 to 282 days' , 2: '283 to 427 days' , 3: 'More than 428 days' , 4: 'Not Previously Contacted'}
        pdays_category = pdays_list[Pdays]


        datanum = [[Balance,Day,Duration,Campaign,Previous]]

        datascale = scaler.transform(datanum)

        # print(datascale)
        
        datainput = [[Job,Marital,Education,Default,datascale[0][0],Housing,Loan,Contact,datascale[0][1],Month,datascale[0][2],datascale[0][3],datascale[0][4],Age,Pdays]]

        pred = model.predict(datainput)[0]

        pred_val = "yes" if pred==1 else "no"


        proba = model.predict_proba(datainput)[0]
        
        if pred == 0:
            proba_val = round((proba[0] * 100), 2)
            open_val = 'Not Open'
        elif pred == 1 :
            proba_val = round((proba[1] * 100), 2)
            open_val = 'Open'

        # Stored Input Data into database.
        query = "insert into customer values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        values = [job_category , mar_category, edu_category, dft_category , balance_val,hos_category , loan_category, cnt_category , day_val , mon_category , dur_val, camp_val , prev_val,  age_category, pdays_category, pred_val]

        cs.execute(query, values)

        db.commit() 
        print(cs.rowcount, "Data Stored Successfully !")


        
        return render_template(
            'Final_Result.html', Job = job_category , Marital = mar_category, Education = edu_category, Default = dft_category , Balance = balance_val, Housing = hos_category ,Loan = loan_category, Contact = cnt_category ,Day = day_val , Month = mon_category , Duration = dur_val, Campaign = camp_val ,Previous = prev_val, Age = age_category, Pdays = pdays_category, pred = pred_val, proba = proba_val, open = open_val
        )

if __name__ == '__main__':
    model = joblib.load("/Users/Andarisa/Desktop/Purwadhika/Final Project/model_LE")
    scaler = joblib.load("/Users/Andarisa/Desktop/Purwadhika/Final Project/Scaler2")
    app.run(debug=True)
