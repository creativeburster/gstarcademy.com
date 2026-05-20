import pandas as pd
import glob
import os

print("=== PARSING LOCAL EXPORTED GSC EXCEL FILES ===")

folder = r"C:\Users\willp\Desktop\26年5月"

# Find our three target files
files = [
    os.path.join(folder, "not found 404.xlsx"),
    os.path.join(folder, "Duplicate without user-selected canonical.xlsx"),
    os.path.join(folder, "Crawled - currently not indexed.xlsx")
]

for f_path in files:
    if os.path.exists(f_path):
        print(f"\n--- File: {os.path.basename(f_path)} ---")
        try:
            # GSC export excel sheets usually have multiple sheets: 'Table', 'Chart', 'Filter' etc.
            # Let's read the 'Table' sheet, which is usually where the URLs are stored
            df = pd.read_excel(f_path, sheet_name=None)
            print("Sheets found:", list(df.keys()))
            
            # Use 'Table' sheet if it exists, otherwise the first sheet
            sheet_name = 'Table' if 'Table' in df.keys() else list(df.keys())[0]
            table_df = df[sheet_name]
            
            print(f"Data columns in '{sheet_name}':", list(table_df.columns))
            # Find a column containing URLs (often has 'URL' or 'Page' in its name)
            url_col = None
            for col in table_df.columns:
                if 'url' in str(col).lower() or 'page' in str(col).lower() or '网址' in str(col).lower():
                    url_col = col
                    break
            
            if url_col:
                print("First 15 URLs:")
                for i, val in enumerate(table_df[url_col].dropna().head(15)):
                    print(f" {i+1}. {val}")
            else:
                print("No URL column found, first 5 rows:")
                print(table_df.head(5))
        except Exception as e:
            print("Error parsing sheet:", e)
    else:
        print(f"File not found: {f_path}")
