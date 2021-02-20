import pandas as pd

mapping_table_string = r'C:\Users\cudolan\desktop\comp_mapping.xlsx'
mapping_table_df = pd.read_excel(mapping_table_string, sheet_name='icd')

print(mapping_table_df.head())