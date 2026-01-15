import json

def list_ram_entries():
    try:
        with open('src/data/vmos.json', 'r') as f:
            data = json.load(f)
            
        print("Searching for RAM entries...")
        found = False
        for item in data:
            # Check makeName, code, model, description for keywords
            s = json.dumps(item).upper()
            if "RAM" in s:
                print(item)
                found = True
        
        if not found:
            print("No RAM entries found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_ram_entries()
