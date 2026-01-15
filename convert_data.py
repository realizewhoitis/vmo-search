import pandas as pd
import json

# List of Major Makes common in the US
MAJOR_MAKES = {
    "ACURA", "ALFA ROMEO", "AUDI", "BMW", "BUICK", "CADILLAC", "CHEVROLET", 
    "CHRYSLER", "DODGE", "FIAT", "FORD", "GENESIS", "GMC", "HONDA", "HUMMER", 
    "HYUNDAI", "INFINITI", "ISUZU", "JAGUAR", "JEEP", "KIA", "LAND ROVER", 
    "LEXUS", "LINCOLN", "MAZDA", "MERCEDES-BENZ", "MERCURY", "MINI", 
    "MITSUBISHI", "NISSAN", "OLDSMOBILE", "PONTIAC", "PORSCHE", "RAM", 
    "SAAB", "SATURN", "SCION", "SMART", "SUBARU", "SUZUKI", "TESLA", 
    "TOYOTA", "VOLKSWAGEN",    "VOLVO"
}

def clean_make_name(name):
    """
    Strips 'administrative' noise from Make Names.
    e.g. 'RAM TRUCKS CHNGD FRM...' -> 'RAM TRUCKS'
    """
    if not name: return ""
    upper_name = name.upper()
    
    # List of separators that start 'noise'
    separators = [
        " PART OF",
        " ALSO SEE",
        " CHNGD",
        " FORMERLY",
        " MAKER OF",
        " DIV ",
        " DIVISION",
        " PREVIOUSLY",
        " COMPANION",
        "("
    ]
    
    cleaned = upper_name
    for sep in separators:
        if sep in cleaned:
            cleaned = cleaned.split(sep)[0]
            
    return cleaned.strip()

# Mapping for some common variations or codes if needed, 
# but for now we'll match against the name roughly.

def convert_vmo_list():
    try:
        # Read Excel file without header
        df = pd.read_excel('../VMO List.xlsx', header=None)
        
        vmos = []
        seen_ids = set()
        current_make = None
        include_current_make = False
        
        for index, row in df.iterrows():
            val0 = str(row[0]).strip() if pd.notna(row[0]) else ""
            val1 = str(row[1]).strip() if pd.notna(row[1]) else ""
            
            # Skip empty lines
            if not val0:
                continue
                
            # Skip Header lines
            if "Model (VM0)" in val0 or "Model (VMO)" in val0:
                continue
                
            # Detect Make (Format: CODE: NAME)
            if ":" in val0 and (not val1 or val1 == "nan"):
                parts = val0.split(":", 1)
                code = parts[0].strip()
                name = parts[1].strip()
                cleaned_name = clean_make_name(name) # Added this line
                
                # Check if this make is in our MAJOR_MAKES list
                make_name_upper = cleaned_name.upper() # Changed from name.upper() to cleaned_name.upper()
                
                if "FORD" in make_name_upper:
                     print(f"DEBUG: Checking potential Ford: {code} - {name}")

                include_current_make = False
                
                # Direct match or starts with (e.g. "FORD TRUCK" vs "FORD")
                for major in MAJOR_MAKES:
                    if major == make_name_upper or make_name_upper.startswith(major + " ") or make_name_upper.endswith(" " + major):
                        include_current_make = True
                        print(f"DEBUG: MATCHED {major} for {cleaned_name}")
                        break
                
                if include_current_make:
                    current_make = {
                        "code": code,
                        "name": cleaned_name
                    }
                    print(f"DEBUG: Found Make: {code} - {current_make['name']}")
                    
                    # Add Make itself as a searchable item
                    vmos.append({
                        "id": f"make-{code}",
                        "type": "make",
                        "code": code,
                        "model": "",
                        "description": cleaned_name,
                        "makeCode": code,
                        "makeName": cleaned_name,
                        "searchTerms": f"{code} {cleaned_name}"
                    })
                else:
                    current_make = None
            
            # Detect Model (if we have a current valid make)
            elif current_make and include_current_make:
                if "FORD" in current_make['name'].upper():
                     print(f"DEBUG: Processing Ford Model: {val0} - {val1}")

                model_code = val0
                # Filter out obvious note lines that are mistakenly treated as codes
                if len(model_code) > 10:
                    print(f"Skipping invalid long code: {model_code}")
                    continue

                description = val1 if val1 and val1 != "nan" else ""
                
                # Filter out invalid or noisy codes
                # 1. Too long (VMOs are usually 3-4 chars)
                if len(model_code) > 8:
                    print(f"Skipping invalid long code: {model_code}")
                    continue
                
                # 2. Contains spaces (Codes are usually alphanumeric)
                if " " in model_code:
                     print(f"Skipping code with spaces: {model_code}")
                     continue

                # Create ID
                item_id = f"model-{current_make['code']}-{model_code}"
                
                # Check for duplicates
                if item_id in seen_ids:
                    print(f"Skipping duplicate ID: {item_id}")
                    continue
                seen_ids.add(item_id)

                vmos.append({
                    "id": item_id,
                    "type": "model",
                    "code": model_code,
                    "model": model_code,
                    "description": description,
                    "makeCode": current_make['code'],
                    "makeName": current_make['name'],
                    "searchTerms": f"{current_make['code']} {current_make['name']} {model_code} {description}"
                })
                
        # Write to src/data/vmos.json
        import os
        os.makedirs('src/data', exist_ok=True)
        
        # Deduplicate entire list just in case (by id)
        unique_vmos = {v['id']: v for v in vmos}.values()
        
        with open('src/data/vmos.json', 'w') as f:
            json.dump(list(unique_vmos), f, indent=2)
            
        print(f"Successfully converted {len(unique_vmos)} items to src/data/vmos.json (Filtered by Major Makes)")
        
    except Exception as e:
        print(f"Error converting file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    convert_vmo_list()
