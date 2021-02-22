import pandas as pd

# import the mapping tables and sql outputs
mapping_table_string = r'C:\Users\cudolan\desktop\comp_mapping.xlsx'
mapping_table_df = pd.read_excel(mapping_table_string, sheet_name='icd')
facilities = pd.read_excel(mapping_table_string, sheet_name='hospital')
msdrg = pd.read_excel(mapping_table_string, sheet_name='ms_drg', dtype=str)
icd = pd.read_excel(mapping_table_string, sheet_name='icd', dtype=str)
df = pd.read_csv('2019-20.csv', 
                names=['Id','Discharge Year','Discharge Date','Discharge Quarter','Admission Year','Admission Date','Hospital ID',
                'ICD - Dx Code','MS-DRG','ICD - Px Code','CPT','Patient ZIP','FIPS Code','Patient County','Inside PSA?','Patient State',
                'Payer Category ID','Payer Category', 'Age','Length of Stay','Admission Source Code','Admission Type/Priority',
                'Discharge Status',	'INPATIENT','OBSERVATION','OP SURGERY','ED','ICU','CCU','NICU-L2','NICU-L3','NICU-L4','Attending','Surgeon','Total Charges',], 
                dtype=str)
print('File Imports -- Complete')


# change columns to int
df['Hospital ID'] = df['Hospital ID'].astype(int)
df['INPATIENT'] = df['INPATIENT'].astype(int)
df['OBSERVATION'] = df['OBSERVATION'].astype(int)
# df['MS-DRG'] = df['MS-DRG'].astype(int)
facilities['Hospital_ID'] = facilities['Hospital_ID'].astype(int)


# vlookup functions
df = pd.merge(df, facilities, how = 'left', left_on = 'Hospital ID', right_on = 'Hospital_ID')
df = pd.merge(df, msdrg, how = 'left', left_on = 'MS-DRG', right_on = 'ms-drg')
df = pd.merge(df, icd, how = 'left', left_on = 'ICD - Dx Code', right_on = 'ICD10')
print('vlookups -- Complete')
# need to add admit source, priority, CPT, Px, Geo mapping, provider names, discharge status


# drop duplicate columns
df = df.drop(['Hospital_ID', 'Street','City', 'County', 'Zip Code', 'ms-drg', 'text_msdrg', 'ms-drg_desc','ICD10', 'icd_desc'], axis = 1)


def return_ip_obs_category(row):
    if row['INPATIENT'] == 1 and row['OBSERVATION'] == 0 and row['ms_drg_in_ex'] == 'Include':
        return 'IP Only'
    if row['INPATIENT'] == 1 and row['OBSERVATION'] == 1 and row['ms_drg_in_ex'] == 'Include':
        return 'IP + OBS'
    if row['INPATIENT'] == 0 and row['OBSERVATION'] == 1 and row['icd_in_ex'] == 'Include':
        return 'OBS Only'
    if row['INPATIENT'] == 1 and row['lurie_spec_group'] == 'Live Births':
        return 'Live Births'
    return 'Exclude'

df['IP_OBS_LB_Exc'] = df.apply(lambda row: return_ip_obs_category(row), axis = 1)
print('Patient Classification -- Complete')


# convert the df to excel
print('Converting to excel')
writer = pd.ExcelWriter('2019-20_data.xlsx', engine='xlsxwriter')
df.to_excel(writer, 'Sheet1')
writer.save()
print('Excel Generation -- Complete')

