import os
import json
import csv
import time
from dotenv import load_dotenv
from openai import OpenAI

# 1. Initialize
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Add your states here. The script will process them 1 by 1.
STATES_LIST = ["Assam", "Uttarakhand"] 

def generate_state_data(state, count=25):
    """Generates a batch of regional food items."""
    prompt = f"""
    Generate a JSON list of {count} unique, pure vegetarian dishes/food items from the state of {state}, India.
    For each item, strictly include these keys:
    "state", "item_name", "rasa", "virya", "vipaka", "dosha_impact", "effect_on_agni", "best_use_case"
    
    Ensure the 'state' field is always '{state}'.
    Return ONLY a JSON object with the key 'food_items'.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a professional Ayurvedic clinical nutritionist."},
                      {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content).get("food_items", [])
    except Exception as e:
        print(f"Error for {state}: {e}")
        return []

def main():
    csv_file = "Master_Ayurveda_Food_Matrix.csv"
    headers = ["state", "item_name", "rasa", "virya", "vipaka", "dosha_impact", "effect_on_agni", "best_use_case"]
    
    # Create the file and write headers ONLY IF it doesn't exist
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
        print(f"Created new file: {csv_file}")

    for state in STATES_LIST:
        print(f"Starting generation for: {state}...")
        
        # Generate 100 items per state in 4 batches of 25
        for batch in range(1, 5):
            items = generate_state_data(state, 25)
            
            if items:
                # 'a' mode appends to the existing file instead of creating a new one
                with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    for item in items:
                        # Ensure every row has the correct state name
                        item['state'] = state
                        row = {h: item.get(h, "N/A") for h in headers}
                        writer.writerow(row)
                print(f"Batch {batch}/4 for {state} saved to master file.")
            
            time.sleep(1) # Prevent API rate limits

    print(f"\nCOMPLETED. All data is now in: {csv_file}")

if __name__ == "__main__":
    main()