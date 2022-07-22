
"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd 
import numpy as np
import random
from random import randrange
from random import randint
from datetime import timedelta
from datetime import date
from mimesis import Field
from mimesis.locales import Locale

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def creer_colonne(classe_variable,size,language=None):
    field=Field(language)
    return [field(classe_variable) for i in range(size)]

def match_pre_made(size,i):
    type_variable=st.selectbox('Wich data do you want ?',('Address','Finance','Datetime','Person','Science'),key=i)
    if type_variable=='Address':
        variable=st.selectbox(f'Which {type_variable} do you want ?',('address','calling_code','city','continent','coordinates','country','federal_subject','latitude','postal_code','province','region','street_name','street_number'),key=i)
    
    elif type_variable=='Finance':
        variable=st.selectbox(f'Which {type_variable} do you want ?',('company','company_type','cryptocurrency_iso_code','currency_symbol'),key=i)
    
    elif type_variable=='Datetime':
        variable=st.selectbox(f'Which {type_variable} do you want ?',('century','day_of_week','formatted_date','month'),key=i)
    
    elif type_variable=='Person':
        variable=st.selectbox(f'Which {type_variable} do you want ?',('academic_degree','blood_type','email','full_name','gender','nationality','occupation','telephone','university'),key=i)
    
    elif type_variable=='Science':
        variable=st.selectbox(f'Which {type_variable} do you want ?',('dna_sequence','mesure_unit'))

    return creer_colonne(variable,size,Locale.EN)

def match_personalized(size,i):

    type=st.selectbox('wich type of data do you want ?',('int','float','categorical'),key=i)
    if type:
        if type=='float'or type=='int':
            loi=st.selectbox('Wich law do you want ?',('uniform','gauss'),key=i)
            if loi== 'uniform' and type =='int':
                max=st.number_input('value max',step=1,key=i)
                min=st.number_input('value min',step=1,key=i)
                if max>min:
                    return [randint(int(min),int(max)) for k in range(size)]
                else:
                    st.write("Warning: max should be superior than min !!")
                    return[0 for k in range(size)]
            elif loi=='uniform' and type=='float':
                max=st.number_input('value max',key=i)
                min=st.number_input('value min',key=i)
                if max>min:
                    return [random.uniform(min,max) for k in range(size)]
                else:
                    st.write("Warning: max should be superior than min !!")
                    return[0 for k in range(size)]

            elif loi=='gauss':
                moy=st.number_input('mean',key=i)
                sig=st.number_input('variance',key=i)
                if type=='int':
                    return [int(random.gauss(moy,sig))  for k in range(size)]
                else:
                    return [random.gauss(moy,sig) for k in range(size)]
        






def creer_variable(size,variables,values,i):
    t=var[i]
    with expander:        
        variables.append(st.text_input('Enter the name of the variable',key=i))
        choice=st.selectbox('which kind of varaible do you want',('pre-made','personalized'),help='With the pre-made: you will use pre-made data base; with the personalized: you will need to provide it',key=i)
        if choice=='pre-made':
            values.append(match_pre_made(size,i))
        else:
            values.append(match_personalized(size,i))



name_file=st.text_input('Insert the name of the new file')
nbre_ligne=int(st.number_input('How many rows do you want ?',step=1000))
nbre_variable=int(st.number_input('How many variables do you want ?',step=0))
values=[]
variables=[]
l=[f'variable{i}'for i in range(nbre_variable)]
var=st.tabs(l)
for i in range(nbre_variable):
    creer_variable(nbre_ligne,variables,values,i)

df_fake_data = pd.DataFrame(dict(zip(variables,values)))
st.write('Sample of the new data set')
st.write(df_fake_data.head())

data_convert=convert_df(df_fake_data)
st.download_button(label="Download data as CSV",data=data_convert,file_name=f'{name_file}.csv',mime='text/csv')

