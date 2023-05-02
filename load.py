
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import pandas as pd
# import mysql.connector
def load1_b():
    # mydb=mysql.connector.connect(host='127.0.0.1',user='root',passwd='Azm123at@1',database='complains')
    # mycursor=mydb.cursor()
    # mycursor.execute('SELECT * FROM complains.customer_complains ')
    # result=mycursor.fetchall()
    # colums_name=['products','issues','sub_products','compliant_ids','timely','company_respopnse','submitted_via','comapnys','date_recive','state','sub_issue']
    # df=pd.DataFrame(result,columns=colums_name)
    # load_dotenv()
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive'] #os.getenv('SCOPE')
    SERVICE_ACCOUNT_FILE = 'D:/Assignment/assignment3.json'#os.getenv('SERVICE_ACCOUNT_FILE')
    SAMPLE_SPREADSHEET_ID = '1JDttND5GyfWqUQ_vG-EmLelfh7JxGLb3VR6LkjyV9LY'#os.getenv('SAMPLE_SPREADSHEET_ID')
    cred=None
    cred = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
    service = build('sheets', 'v4', credentials=cred)
    sheet =  service.spreadsheets()


    result=sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='state!A1:L'
                        ).execute()
    values = result.get('values', [])
    columns_name=[name for name in values[0]]
    print(len(columns_name))
    data={columns_name[0]:[],columns_name[1]:[],columns_name[2]:[],columns_name[3]:[],columns_name[4]:[],columns_name[5]:[],
          columns_name[6]:[],columns_name[7]:[],columns_name[8]:[],columns_name[9]:[],columns_name[10]:[]}
    for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            data[columns_name[0]].append(row[0])
            data[columns_name[1]].append(row[1])
            data[columns_name[2]].append(row[2])
            data[columns_name[3]].append(row[3])
            data[columns_name[4]].append(row[4])
            data[columns_name[5]].append(row[5])
            data[columns_name[6]].append(row[6])
            data[columns_name[7]].append(row[7])
            data[columns_name[8]].append(row[8])
            data[columns_name[9]].append(row[9])
            try:
                data[columns_name[10]].append(row[10])
            except:
                 data[columns_name[10]].append(" ")
    data=pd.DataFrame(data)
    return data




