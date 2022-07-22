import streamlit as st
import pandas as pd 
import numpy as np
import random

from datetime import date
from mimesis import Field
from mimesis.locales import Locale
from io import BytesIO

def create_matrix(n):
	return [[] for k in range(n)]

def get_windows(nbre_variable):
	for i in range(nbre_variable):
		if f'variable n°{i}' not in st.session_state:
			st.session_state[f'variable n°{i}']=f'variable n°{i+1}'
	return st.tabs([st.session_state[f'variable n°{i}'] for i in range(nbre_variable)])

def get_Names_Info(nbre_variable):
	
	
	windows=get_windows(nbre_variable)
	Name_variables=[]
	Info_variables=create_matrix(nbre_variable)
    
	for i in range(nbre_variable):
		with windows[i]:
			l,r=st.columns(2)
			l.text_input('Enter the name of the variable',key=f'variable n°{i}')
			Name_variables.append(st.session_state[f'variable n°{i}'])
			choice=r.selectbox('Which varaible do you want ?',('pre-made','personalized'),help='With the pre-made: you will use pre-made data base; with the personalized: you will need to provide it',key=i)
			Info_variables[i].append(choice)
			if choice=='pre-made':
				l,r=st.columns(2) 
				type_variable=l.selectbox('Wich data do you want ?',('Address','Finance','Datetime','Person','Science'),key=i)
				lov_categories = ['Address','Finance','Datetime','Person','Science']
				address_lovs = ('address','calling_code','city','continent','coordinates','country','federal_subject','latitude','postal_code','province','region','street_name','street_number')
				finance_lovs = ('company','company_type','cryptocurrency_iso_code','currency_symbol')
				datetime_lovs = ('century','day_of_week','formatted_date','month')
				person_lovs = ('academic_degree','blood_type','email','full_name','gender','nationality','occupation','telephone','university')
				science_lovs = ('dna_sequence')
				lovs = [address_lovs, finance_lovs, datetime_lovs, person_lovs, science_lovs]
				dict_lovs = dict(zip(lov_categories, lovs))
				variable=r.selectbox(f'Which {type_variable} do you want ?', dict_lovs[type_variable], key=i)
				Info_variables[i].append(variable)

			else:
				type_variable=l.selectbox('wich type of data do you want ?',('int','float','categorical'),key=f'type{i}')
				Info_variables[i].append(type_variable)

				if type_variable=='float'or type_variable=='int':
					loi=r.selectbox('Wich law do you want ?',('uniform','gauss'),key=f'law{i}')
					Info_variables[i].append(loi)
					if loi=='uniform' :
						max_=l.number_input('value max',key=f'max{i}')
						min_=r.number_input('value min',key=f'min{i}')
						Info_variables[i].append((max_,min_))
					elif loi=='gauss':
						moy=l.number_input('mean',key=f'moy{i}')
						sig=r.number_input('standard error',key=f'sig{i}')
						Info_variables[i].append((moy,sig))
				else:
					nbre_category=r.number_input('How many category ?',min_value=1,max_value=12,step=1,key=f'nbre_category{i}')
					liste=[]
					list_weigh=[]
					columns=st.columns(6)
					for m in range(int(nbre_category//3)):
						for w in range(3):
							liste.append(columns[2*w].text_input('Category',key=f'quotient{i}{w}{m}'))
							list_weigth.append(columns[2*w+1].number_input('Weight',min_value=1,step=1,key=f'weight_quotient{i}{w}{m}'))
					for j in range(int(nbre_category%3)):
						liste.append(columns[2*j].text_input('Category',key=f'rest{i}{j}'))
						list_weigth.append(columns[2*j+1].number_input('Weight',min_value=1,step=1,key=f'weight_rest{i}{j}'))

					Info_variables[i].append(liste)
					Info_variables[i].append(list_weigth)

	return (Name_variables,Info_variables)


def get_values(Info_variables,nbre_ligne,nbre_variable):
	res=[]
	for i in range(nbre_variable):
		if Info_variables[i][0]=='pre-made':
			field=Field(Locale.EN)
			_res=[field(Info_variables[i][1]) for k in range(nbre_ligne)]
		else:
			if Info_variables[i][1]=='float' or Info_variables[i][1]=='int':
				if Info_variables[i][2]=='uniform':
					mi,ma=Info_variables[i][3]
					if Info_variables[i][1]=='float':
						_res= [random.uniform(mi,ma) for k in range(nbre_ligne)]
					else:
						_res= [random.randint(int(mi),int(ma)) for k in range(nbre_ligne)]

				elif Info_variables[i][2]=='gauss':
					moy,sig=Info_variables[i][3]
					if Info_variables[i][1]=='float':
						_res= [random.gauss(moy,sig) for k in range(nbre_ligne)]
					else:
						_res= [int(random.gauss(int(moy),int(sig))) for k in range(nbre_ligne)]
			else:
				_res = random.choices(Info_variables[i][2],weigths=Info_variables[i][3],k=nbre_ligne)

		res.append(_res)
	return res


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def main():
	st.title('Fake_Data_Generator')
	l,c,r=st.columns(3)
	
	name_file=l.text_input('Insert the name of the new file')
	nbre_ligne=int(c.number_input('How many rows do you want ?',step=1000))
	nbre_variable=int(r.number_input('How many variables do you want ?',min_value=1,step=1))


	Name_variables,Info_variables=get_Names_Info(nbre_variable)
	Values_Sample=get_values(Info_variables,5,nbre_variable)
	

	Sample = pd.DataFrame(dict(zip(Name_variables,Values_Sample)))
	st.write('Sample of the new data set')
	st.write(Sample.head())
	le,ce,ri=st.columns(3)

	if le.button('Create the new Data Set '):

		Values=get_values(Info_variables,nbre_ligne,nbre_variable)
		df_fake_data=pd.DataFrame(dict(zip(Name_variables,Values)))
		csv= convert_df(df_fake_data)
		df_excel = to_excel(df_fake_data)
				   
		ce.download_button(label="📥 Download (.csv)",data=csv,file_name=f'{name_file}.csv',mime='text/csv')
		ri.download_button(label="📥 Download (.xlsx)",data=df_excel,file_name=f'{name_file}.xlsx',mime='text/xlsx')
main()


