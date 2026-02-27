# Fix for UnicodeDecodeError when reading Excel files
# The error occurs when trying to read .xlsx files with pd.read_csv()

import pandas as pd
import os

print("Current working directory:", os.getcwd())
print("Files in directory:", os.listdir('.'))

# WRONG WAY (causes UnicodeDecodeError):
# cu_df = pd.read_csv('Final_CU_List.xlsx')  # Don't use this for Excel files!

# CORRECT WAY for Excel files:
try:
    cu_df = pd.read_excel('Final_CU_List.xlsx')
    
    print("\n✅ Excel file read successfully!")
    print(f"Shape: {cu_df.shape}")
    print(f"Columns: {list(cu_df.columns)}")
    print("\nFirst 5 rows:")
    print(cu_df.head())
    
except FileNotFoundError:
    print("❌ File not found. Make sure 'Final_CU_List.xlsx' is in the current directory.")
except Exception as e:
    print(f"❌ Error reading file: {e}")