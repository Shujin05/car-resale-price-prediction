import pandas as pd

# Load datasets
carsome_data = pd.read_csv('carsome_data.csv')
carsome_df = pd.DataFrame(carsome_data)

carlist_data = pd.read_csv('carlist_data.csv')
carlist_df = pd.DataFrame(carlist_data)

def clean_mileage_carsome(value):
    parts = value.split()
    cleaned = parts[0]
    return clean_to_int(cleaned)

def clean_mileage_carlist(value):
    if '-' in value: 
        parts = value.split('-')
        min_mileage = int(parts[0].strip())
        max_mileage = int(parts[1].split("K")[0])
        avg = (min_mileage + max_mileage)//2 
        avg = avg*1000
        return int(avg)
    else: 
        parts = value.split()
        cleaned = parts[0]
        return int(cleaned)

def clean_year_carlist(value):
    if '/' in value: 
        return convert_int(value.split('/')[0])
    else:
        return convert_int(value)

def clean_to_int(value):
    return int(value.replace(",", ""))

def convert_int(value):
    return int(value)

# Apply the cleaning functions to carsome_df
carsome_df['Price'] = carsome_df['Price'].apply(clean_to_int)
carsome_df['Mileage'] = carsome_df['Mileage'].apply(clean_mileage_carsome)
carsome_df['Year'] = carsome_df['Year'].apply(convert_int)

# Apply the cleaning functions to carlist_df
carlist_df['Price'] = carlist_df['Price'].apply(clean_to_int)
carlist_df['Mileage'] = carlist_df['Mileage'].apply(clean_mileage_carlist)
carlist_df['Year'] = carlist_df['Year'].apply(clean_year_carlist)

# Save to new csvs
carsome_df.to_csv('cleaned_carsome_data.csv', index=False)
carlist_df.to_csv('cleaned_carlist_data.csv', index=False)