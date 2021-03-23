import pandas as pd

mapping_table_str = r'C:\Users\cudolan\desktop\appt_mapping.xlsx'
sql_file_str = r'H:\00-My Documents\SQL Text Files\appt_test_1.csv'
site_mapping_df = pd.read_excel(mapping_table_str, sheet_name = 'site')
pt_origin_df = pd.read_excel(mapping_table_str, sheet_name = 'pt_origin')
exam_rm_df = pd.read_excel(mapping_table_str, sheet_name = 'not_in_exam_room')


dept_grouping_df = pd.read_excel(mapping_table_str, sheet_name = 'dept_grouping')

df = pd.read_csv(sql_file_str, names = ['Appt Date','Appt FY','Appt FY Qtr',
            'AM/PM/Evening','Weekday Num','Weekday Name', 'Week Day Occurrence Number', 'Week of Month',
            'Appt Made Date','Appt Cancelled Date','Lag Time','Time Cancelled Prior to Appt (Days)',
            'HAR','MRN','Pt Zip Code','Appt Status ID','Appt Status','Same Day Cancellation',
            'Detailed Appt Type','NEW/RETURN/OTHER','Appt Length','Appt Notes','Cancellation Reason',
            'Division','Site','Site Abbreviation','Epic Dept','Attending Provider','PCP ID',
            'Primary Dx','Primary Dx DESC','Payer ID','Medicaid/NonMed'])


df = pd.merge(df, site_mapping_df, how = 'left', left_on = 'Epic Dept', right_on = 'site_department')
df = pd.merge(df, pt_origin_df, how = 'left', left_on = 'Pt Zip Code', right_on = 'pt_zip_code')
df = pd.merge(df, exam_rm_df, how = 'left', left_on = 'Detailed Appt Type', right_on = 'examrm_appt_type')
df = pd.merge(df, dept_grouping_df, how = 'left', left_on = 'Division', right_on = 'division')

df['Appt FY'] = df['Appt FY'].astype(str)
df['Appt FY Qtr'] = df['Appt FY Qtr'].astype(str)
df['Week of Month'] = df['Week of Month'].astype(str)
df['Weekday Name'] = df['Weekday Name'].astype(str)
df['Week Day Occurrence Number'] = df['Week Day Occurrence Number'].astype(str)

# handle if there is another zipcode or blank
df['FY - Qtr'] = 'FY' + df['Appt FY']+' - ' + df['Appt FY Qtr']
df['WkNum + WkDay'] = df['Week of Month'].map(str) + ' - ' + df['Weekday Name']
df[' DayNum + WkDay'] = df['Week Day Occurrence Number'].map(str) + ' - ' + df['Weekday Name']

df = df.drop(['Appt FY', 'Appt FY Qtr', 'Weekday Name' ,'site_department','Site Abbr.', 'pt_zip_code',
            'examrm_appt_type', 'division'], axis = 1)


writer = pd.ExcelWriter('appt_test.xlsx', engine='xlsxwriter')
df.to_excel(writer, 'Sheet1', index = False)
writer.save()
