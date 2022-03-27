import pandas as pd
import numpy as np

from currency_converter import CurrencyConverter
currency_converter_obj = CurrencyConverter()

def load_data(excel_file):
    df_input = pd.read_excel(excel_file, sheet_name="Form responses 1")

    rename_dict = {
        "Timestamp" : "timestamp",
        "Gender" : "gender",
        "Age" : "age",
        "Current Country of Residence" : "country",
        "Current State of Residence" : "state",
        "Highest Level of Education" : "edu_level",
        "Did you go through a bootcamp to learn technical skills?" : "bootcamp_attended",
        "Professional Certification (Eg. CCNA, CEH, GCP Cloud Associate)": "professional_cert_taken",
        "Is your degree tech related?": "edu_tech_related",
        "What technologies do you use for work on a regular basis?": "tech_used",
        "Job Title": "role_position",
        "What is your currency code?": "currency_code_salary",
        "What is your current monthly base salary?": "salary",
        "Indicate in 3-character currency code for starting monthly salary": "currency_code_salary_start",
        "What was your starting monthly salary?": "salary_start"
    }

    df_input = df_input.rename(columns = rename_dict)
    df_input["role_position"] = df_input["role_position"].str.strip()
    df_input = df_input.replace('', np.nan, regex=True)
    df_input = df_input.dropna(subset=['role_position'])
    
    df_input['state'] = df_input['state'].apply(clean_state_list)
    
    df_input["converted_salary"] = df_input.apply(df_currency_convert, axis=1)
    df_input = df_input[df_input['converted_salary'].notna()]

    df_input['edu_tech_related'] = df_input['edu_tech_related'].apply(check_true_or_false)
    df_input['bootcamp_attended'] = df_input['bootcamp_attended'].apply(check_true_or_false)
    df_input['professional_cert_taken'] = df_input['professional_cert_taken'].apply(check_true_or_false)

    return df_input
    
    
def clean_state_list(state_input):
    if not isinstance(state_input, str): 
        return state_input
        
    # states and its alternative name
    malaysia_state = {
      "Johor": ["JB","Muar","Iskandar"],
      "Kedah": ["Alor Setar","Kulim","Sungai Petani"],
      "Kelantan": ["Kota Bahru","Kota Baru"],
      "Melaka": [],
      "Negeri Sembilan": [],
      "Pahang": [],
      "Perak": ["Ipoh","Taiping"],
      "Perlis": [],
      "Pulau Pinang": ["Penang","PG","Pinang","George Town", "Georgetown", "Bayan Lepas"],
      "Sarawak": [],
      "Selangor": ["PJ", "Petaling Jaya", "Subang"],
      "Terengganu": [],
      "Kuala Lumpur": ["KL", "Wilayah", "Setapak"],
      "Labuan": [],
      "Sabah": [],
      "Putrajaya": ["Cyberjaya", "Cyber"]
    }
    
    for state in malaysia_state:
        if state.lower() in state_input.lower():
            return state
        
        for alternative_name in malaysia_state[state]:
            if alternative_name.lower() in state_input.lower():
                return state
            
    return "Others" 


def currency_convert(currency_type, currency_value):
    currency_type = currency_type.upper()
    if currency_type != "MYR":
        try:
            return currency_converter_obj.convert(currency_value, currency_type, 'MYR')
        except:
            return np.nan
    else:
        return currency_value
        

def check_true_or_false(value_input):
    value_input = str(value_input)
    if value_input.lower() in ['yes','ya','yeah','true']:
        return True
    else:
        return False
 
def df_currency_convert(row):
    return currency_convert(row['currency_code_salary'], row['salary'])
    
    