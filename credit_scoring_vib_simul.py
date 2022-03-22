# -*- coding: utf-8 -*-
"""credit scoring vib simul.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YD_eObHFuoHmKFlvHDVxfTWNppmBjbDI
"""



import pandas as pd
import scipy as sp
import numpy as np
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
import streamlit as st




def housing_time(df):
  condition = [
             (df['age']<20),#Less than 1 year
             (df['age']>=20)&(df['age']<24), #1-3 years
             (df['age']>=24)&(df['age']<35),#3-6 years
             (df['age']>=35)&(df['age']<50),#6-10 years
             (df['age']>=50)]
  choice =['less_1_years', '1-3_years','3-6_years','6-10_years','over_10_years']
  df['housing_time'] = np.select(condition, choice)
  return df['housing_time']

def income(df):
  conditions = [ 
              (df['job']=='skilled employee') ,
              (df['job']=='unskilled resident') ,
              (df['job']=='mangement self-employed') ,(df['job']=='unemployed non-resident')]
  values = ['>8mill','5-8mil','3-5mil','2-3mil']
  df['Income'] = np.select(conditions, values)
  return df['Income']

def education(df):
  np.random.seed(445)
  df['education'] = np.random.choice(  
     a=['over_university_aboard', 'over_university_country', 'university','highschool'],  
    size=1000,  
     p=[0.1, 0.2, 0.5, 0.2] ) 
  return df['education']

def preprocess(df):
  df['amount'] = df['amount']*13346
  df = df.rename(columns={'default':'TARGET'})
  df['TARGET'].replace({2:1,1:0}, inplace=True)
  df['employment_length'].replace({'1 - 4 yrs':'1-3_years', '> 7 yrs':'>5_years','4 - 7 yrs':'3-5_years',
                                 '0 - 1 yrs':'0-1_years'},inplace=True)
  df = df.astype({"existing_credits":'category'})

  df['existing_credits'].replace({1:'1_vib_card',2:'2_vib_card', 3:'another_bank', 4:'another_bank'}, inplace=True)

  df['monthly_payment'] = (df['amount']*(df['installment_rate']/1200)*(1+df['installment_rate']/1200)**(df['months_loan_duration']))/((1+df['installment_rate']/1200)**(df['months_loan_duration'])-1)
  df['monthly_payment'] =round(df['monthly_payment'],0)

  df['housing_time'] = round(df['age']/df['residence_history'],0)
  if (df['residence_history'] == 1).any():df['housing_time']=df['age']

  df['housing_time'] = housing_time(df)
  df['Income'] = income(df)
  df['education']  = education(df)
  credit_vib = df[['age','education', 'dependents','personal_status','housing','housing_time','employment_length','job','existing_credits','Income','monthly_payment','TARGET']]
  return credit_vib

def age(df):
  conditions = [ 
              (df['age']<21) & (df['age']>=18),
              (df['age']<30) & (df['age']>=21),
              (df['age']>=30) & (df['age']<50),
              (df['age']>=60) & (df['age']<60)]
  values = [5, 6, 9, 8]
  Scoring_board['AGE_POINT'] = np.select(conditions, values)
  return Scoring_board['AGE_POINT']


def education_point(df):
  conditions = [ 
              (df['education']=='university'),
              (df['education']=='over_university_country'),
              (df['education']=='highschool'),
              (df['education']=='over_university_aboard')]
  values = [7, 8, 5, 9]
  Scoring_board['EDU_POINT'] = np.select(conditions, values)
  return Scoring_board['EDU_POINT']

def CHILD(df):
  conditions = [ 
              (df['dependents']==0),
              (df['dependents']==1),
              (df['dependents']==2),
              (df['dependents']==3),
              (df['dependents']>=4)]
  values = [5, 8, 7, 6, 4]
  Scoring_board['CHILD_POINT'] = np.select(conditions, values)
  return Scoring_board['CHILD_POINT']

def FAM_STATUS(df):
  conditions = [ 
              (df['personal_status']=='single male'),
              (df['personal_status']=='female'),
              (df['personal_status']=='married male'),
              (df['personal_status']=='divorced male')]
  values = [7, 7, 9, 6]
  Scoring_board['FAM_STATUS_POINT'] = np.select(conditions, values)
  return Scoring_board['FAM_STATUS_POINT']

def housing(df):
  conditions = [ 
              (df['housing']=='own'),
              (df['housing']=='rent'),
              (df['housing']=='for free')]
  values = [9, 4, 6]
  Scoring_board['HOUSING_POINT'] = np.select(conditions, values)
  return Scoring_board['HOUSING_POINT']

def HOUSING_TIME_POINT(df):
  conditions = [ 
              (df['housing_time']=='less_1_years'),
              (df['housing_time']=='1-3_years'),
              (df['housing_time']=='3-6_years'),
              (df['housing_time']=='6-10_years'),
              (df['housing_time']=='over_10_years')]
  values = [6, 7, 8, 9, 10]
  Scoring_board['HOUSING_TIME_POINT'] = np.select(conditions, values)
  return Scoring_board['HOUSING_TIME_POINT']

def EMP_length_point(df):
  conditions = [ 
              (df['employment_length']=='1-3_years'),
              (df['employment_length']=='>5_years'),
              (df['employment_length']=='3-5_years'),
              (df['employment_length']=='0-1_years'),
              (df['employment_length']=='unemployed')]
  values = [7, 9, 8, 6, 0]
  Scoring_board['EMP_length_point'] = np.select(conditions, values)
  return Scoring_board['EMP_length_point']

def job_point(df):
  conditions = [ 
              (df['job']=='mangement self-employed'),
              (df['job']=='skilled employeet'),
              (df['job']=='unskilled resident'),
              (df['job']=='unemployed non-resident')]
  values = [9, 8, 7, 0]
  Scoring_board['job_point'] = np.select(conditions, values)
  return Scoring_board['job_point']
  
def existing_credits_point(df):
  conditions = [ 
              (df['existing_credits']=='1_vib_card'),
              (df['existing_credits']=='2_vib_card'),
              (df['existing_credits']=='another_bank')]
  values = [7, 8, 6]
  Scoring_board['existing_credits_point'] = np.select(conditions, values)
  return Scoring_board['existing_credits_point']

def Income(df):
  conditions = [ 
              (df['Income']=='>8mill'),
              (df['Income']=='5-8mil'),
              (df['Income']=='3-5mil'),
              (df['Income']=='2-3mil')]
  values = [9, 8, 7, 5]
  Scoring_board['Income_point'] = np.select(conditions, values)
  return Scoring_board['Income_point']

def monthly_payment_POINT(df):
  conditions = [ 
              (df['monthly_payment']<500000),
              (df['monthly_payment']>=500000)&(df['monthly_payment']<1000000),
              (df['monthly_payment']>=1000000)&(df['monthly_payment']<3000000),
              (df['monthly_payment']>=3000000)&(df['monthly_payment']<5000000),
              (df['monthly_payment']>=5000000)]
  values = [5, 6, 8, 9, 10]
  Scoring_board['monthly_payment_POINT'] = np.select(conditions, values)
  return Scoring_board['monthly_payment_POINT']

Scoring_board = pd.DataFrame()
def weighted_scoring(df):
  Scoring_board['AGE_POINT'] = age(df)
  Scoring_board['EDU_POINT'] = education_point(df)
  Scoring_board['CHILD_POINT'] = CHILD(df)
  Scoring_board['FAM_STATUS_POINT'] = FAM_STATUS(df)
  Scoring_board['job_point'] = job_point(df)
  Scoring_board['HOUSING_POINT'] = housing(df)
  Scoring_board['HOUSING_TIME_POINT'] = HOUSING_TIME_POINT(df)
  Scoring_board['EMP_length_point'] = EMP_length_point(df)
  Scoring_board['existing_credits_point'] = existing_credits_point(df)
  Scoring_board['Income_point'] = Income(df)
  Scoring_board['monthly_payment_POINT'] = monthly_payment_POINT(df)
  Scoring_board['credit_point'] = 0.04*Scoring_board['AGE_POINT'] + 0.05*Scoring_board['EDU_POINT'] + 0.05*Scoring_board['CHILD_POINT']+0.05*Scoring_board['FAM_STATUS_POINT']+0.15*Scoring_board['HOUSING_POINT']+0.03*Scoring_board['HOUSING_TIME_POINT']+0.04*Scoring_board['EMP_length_point']+0.05*Scoring_board['job_point']+0.05*Scoring_board['existing_credits_point']+0.35*Scoring_board['Income_point']+0.05*Scoring_board['monthly_payment_POINT']
  return Scoring_board


def result(Scoring_board, df) :
  conditions = [ 
              (Scoring_board['credit_point']>7),
              (Scoring_board['credit_point']<=7)]
  
  values = [0, 1]
  df['ESTIM_TARGET'] = np.select(conditions, values)
  df = df.groupby('TARGET', group_keys=False).apply(lambda x: x.sample(frac=0.2))
  #plot
  domain_fpr, domain_tpr, domain_threshold = metrics.roc_curve(df.TARGET, df.ESTIM_TARGET)
  domain_roc_auc = metrics.auc(domain_fpr, domain_tpr)
  a = plt.title('Receiver Operating Characteristic')
  plt.plot(domain_fpr, domain_tpr, '^', label='domain (AUC = %0.2F)' % domain_roc_auc)
  plt.legend(loc = 'lower right')
  plt.plot([0, 1], [0, 1],'r--')
  plt.xlim([0, 1])
  plt.ylim([0, 1])
  plt.ylabel('True Positive Rate')
  plt.xlabel('False Positive Rate')
  plt.show()
  return plt # print(classification_report(df.TARGET, df.ESTIM_TARGET)),

def display(st,result):
    # st.set_page_config(page_title='Khuyến nghị giao dịch cổ phiếu', page_icon=None,layout="wide",initial_sidebar_state='auto')
    col1 = st.beta_columns(1)
    with col1:
        st.plotly_chart(result)
        st.markdown('<p style="font: 16px bold Georgia, serif; text-transform: uppercase; color: blue;text-align: center;">credit</p>',unsafe_allow_html=True)
        st.table(exportList2.assign(hack='').set_index('hack'))


if __name__ == "__main__":
    df= pd.read_csv('./credit.csv')
    preprocess = preprocess(df=df)
    weighted_df = weighted_scoring(preprocess=preprocess)
    result = result(Scoring_board=weighted_df, df=preprocess)
    display(st, result=result)
