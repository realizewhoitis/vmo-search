import json
from collections import defaultdict

def check_duplicates():
    try:
        with open('src/data/vmos.json', 'r') as f:
            data = json.load(f)
            
        code_map = defaultdict(set)
        
        for item in data:
            if item['type'] == 'model':
                # Map code to the set of makes it belongs to
                code_map[item['code']].add(item['makeName'])
        
        duplicates = {code: makes for code, makes in code_map.items() if len(makes) > 1}
        
        if duplicates:
            print(f"Found {len(duplicates)} codes that repeat across different makes:")
            for code, makes in list(duplicates.items())[:20]: # Show top 20
                print(f"Code '{code}' appears in: {', '.join(makes)}")
            if len(duplicates) > 20:
                print(f"...and {len(duplicates) - 20} more.")
        else:
            print("No duplicate codes found across different makes.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_duplicates()
