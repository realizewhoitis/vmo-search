import pandas as pd

def check_econoline():
    try:
        df = pd.read_excel('../VMO List.xlsx', header=None)
        print("Searching for 'ECONOLINE' in Excel...")
        
        found = False
        for index, row in df.iterrows():
            row_str = str(row.values).upper()
            if "ECONOLINE" in row_str:
                print(f"Found at row {index}: {row_str}")
                found = True
                
        if not found:
            print("ECONOLINE not found in Excel file.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_econoline()
