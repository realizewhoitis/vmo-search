import pandas as pd

def inspect_around_econoline():
    try:
        df = pd.read_excel('../VMO List.xlsx', header=None)
        # Slicing around row 1240 (0-indexed, so 1239 roughly)
        # Let's verify the row index from previous step.
        # "Found at row 1240"
        
        start = max(0, 1200)
        end = 1250
        print(f"Rows {start} to {end}:")
        print(df.iloc[start:end])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_around_econoline()
