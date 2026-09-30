import pandas as pd
from numbers_parser import Document

doc = Document('/Users/naman/Desktop/Automation/new list student .numbers')
sheets = doc.sheets
tables = sheets[0].tables
data = tables[0].rows(values_only=True)

df = pd.DataFrame(data[1:], columns=data[0])
print(df.head())
df.to_csv('students_data.csv', index=False)
