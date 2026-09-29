import pandas as pd

def print_markdown_table(filepath):
    try:
        df = pd.read_excel(filepath)
        df.columns = df.columns.str.strip()
        class_6_students = df[df['Class'].astype(str).str.contains('Sixth', case=False, na=False)].fillna('N/A')
        
        print("| Sr No | Name | DOB | Father's Name | Mother's Name | Mobile |")
        print("|---|---|---|---|---|---|")
        
        for index, row in class_6_students.iterrows():
            sr = row.get('Sr No.', index)
            name = row.get('FullName as on Aadhar Card', row.get('FullName', 'Unknown'))
            dob = row.get('Date of Birth', 'Unknown')
            if hasattr(dob, 'strftime'):
                dob = dob.strftime('%b %d, %Y')
            father_name = row.get("Father's Full Name aso on Aadhar Card", 'Unknown')
            mother_name = row.get("Mother's Full Name as on Aadhaar", 'Unknown')
            mobile = row.get("Father's Mobile No", 'N/A')
            if mobile != 'N/A' and mobile != '':
                mobile = str(mobile).replace('.0', '')
                
            print(f"| {sr} | {name} | {dob} | {father_name} | {mother_name} | {mobile} |")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print_markdown_table("StudentListingReport (24).xlsx")
