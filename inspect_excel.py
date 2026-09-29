import pandas as pd
import json
import sys

def inspect_excel(filepath):
    print(f"Inspecting file: {filepath}\n")
    try:
        excel_file = pd.ExcelFile(filepath)
        print(f"Sheet names: {excel_file.sheet_names}\n")
        
        for sheet in excel_file.sheet_names:
            print(f"--- Sheet: {sheet} ---")
            df = pd.read_excel(filepath, sheet_name=sheet)
            print(f"Rows: {len(df)}")
            print(f"Columns: {len(df.columns)}")
            
            if not df.empty:
                print("Columns:")
                for col in df.columns:
                    col_type = str(df[col].dtype)
                    null_count = df[col].isnull().sum()
                    print(f"  - {col}: type={col_type}, nulls={null_count}")
                
                print("\nSample Data (first 3 rows):")
                print(df.head(3).to_string())
            print("\n")
            
    except Exception as e:
        print(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    inspect_excel("StudentListingReport (24).xlsx")
