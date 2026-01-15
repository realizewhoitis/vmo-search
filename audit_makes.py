import pandas as pd

# Same list as in convert_data.py
MAJOR_MAKES = {
    "ACURA", "ALFA ROMEO", "AUDI", "BMW", "BUICK", "CADILLAC", "CHEVROLET", 
    "CHRYSLER", "DODGE", "FIAT", "FORD", "GENESIS", "GMC", "HONDA", "HYUNDAI", 
    "INFINITI", "JAGUAR", "JEEP", "KIA", "LAND ROVER", "LEXUS", "LINCOLN", 
    "MAZDA", "MERCEDES-BENZ", "MINI", "MITSUBISHI", "NISSAN", "PORSCHE", "RAM", 
    "SUBARU", "TESLA", "TOYOTA", "VOLKSWAGEN", "VOLVO"
}

def audit_makes():
    try:
        df = pd.read_excel('../VMO List.xlsx', header=None)
        
        kept_makes = set()
        dropped_makes = set()
        
        for index, row in df.iterrows():
            val0 = str(row[0]).strip() if pd.notna(row[0]) else ""
            val1 = str(row[1]).strip() if pd.notna(row[1]) else ""
            
            if not val0: continue
            if "Model (VM0)" in val0 or "Model (VMO)" in val0: continue
            
            # Identify Makes
            if ":" in val0 and (not val1 or val1 == "nan"):
                parts = val0.split(":", 1)
                name = parts[1].strip()
                make_name_upper = name.upper()
                
                is_kept = False
                for major in MAJOR_MAKES:
                    if major == make_name_upper or make_name_upper.startswith(major + " ") or make_name_upper.endswith(" " + major):
                        is_kept = True
                        break
                
                if is_kept:
                    kept_makes.add(name)
                else:
                    dropped_makes.add(name)
                    
        print(f"KEPT MAKES ({len(kept_makes)}):")
        print("\n".join(sorted(list(kept_makes))))
        print("-" * 40)
        print(f"DROPPED MAKES ({len(dropped_makes)}):")
        print("\n".join(sorted(list(dropped_makes))))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    audit_makes()
