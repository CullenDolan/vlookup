import pandas as pd

facilities = pd.read_excel('comp_mapping.xlsx', sheet_name='hospital')
msdrg = pd.read_excel('comp_mapping.xlsx', sheet_name='ms_drg', dtype=str)
icd = pd.read_excel('comp_mapping.xlsx', sheet_name='icd', dtype=str)
df = pd.read_csv('2019 adv.csv', 
                names=['Id','Discharge Year','Discharge Date','Discharge Quarter','Admission Year','Admission Date','PROVIDER FACILITY',
                'ICD - Dx Code','MS-DRG','ICD - Px Code','CPT','Patient ZIP','FIPS Code','Patient County','Inside PSA?','Patient State',
                'Payer Category ID','Payer Category','PATIENT TYPE','Age','Length of Stay','Admission Source Code','Admission Type/Priority',
                'Discharge Status',	'INPATIENT','OBSERVATION','OP SURGERY','ED','ICU','CCU','NICU-L2','NICU-L3','NICU-L4','Attending','Surgeon','Total Charges',], 
                dtype=str)

df['PROVIDER FACILITY'] = df['PROVIDER FACILITY'].astype(int)
facilities['Provider_ID'] = facilities['Provider_ID'].astype(int)

df = pd.merge(df, facilities, how = 'left', left_on = 'PROVIDER FACILITY', right_on = 'Provider_ID')
df = pd.merge(df, msdrg, how = 'left', left_on = 'MS-DRG', right_on = 'text_msdrg')
df = pd.merge(df, icd, how = 'left', left_on = 'ICD - Dx Code', right_on = 'ICD10')

df = df.drop(['Provider_ID', 'Street','City', 'County', 'Zip Code', 'ms-drg', 'text_msdrg', 'ms-drg_desc','ICD10', 'icd_desc'], axis = 1)


print('converting to excel')
writer = pd.ExcelWriter('2019_adv_data.xlsx', engine='xlsxwriter')
df.to_excel(writer, 'Sheet1')
writer.save()