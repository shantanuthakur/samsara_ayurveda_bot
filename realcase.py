import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

THEMES = [
    "PCOS (Kapha-Pitta imbalance)", "Hypothyroidism (Agni Mandya)", 
    "Weight Loss (Meda Dhatu reduction)", "Weight Gain (Brimhana Therapy)", 
    "IBS/Bloating (Vata-Agni)", "Hyperacidity/GERD (Pitta aggravation)",
    "Modern Stress & Insomnia", "Skin/Acne (Rakta-Pitta)", "Postpartum Strength"
]

REGIONS = ["Assam", "Uttarakhand", "Punjab", "South India", "Maharashtra", "West Bengal"]

def generate_clinical_batch(count=5, theme="General", region="India"):
    """Generates a batch with strict key enforcement for Instruction/Input/Output."""
    
    prompt = f"""
    Generate {count} unique clinical training cases in JSON format for an Ayurvedic bot.
    Theme: {theme} | Region: {region}
    
    STRICT CONSTRAINTS:
    1. Diet MUST be **Pure Vegetarian** (No meat, fish, or eggs).
    2. The 'input' field MUST contain the full profile (13 parameters: Age, Gender, Weight, Height, BMI, Goals, Symptoms, Cycle, Lifestyle, Food habits, Dosha, Pre-existing issues, Stress).
    3. The 'output' MUST include exact quantities (gm/ml) for every food item.
    4. Include 'Red Flags' (e.g., TSH > 10 triggers urgent referral).

    Format each case as an object with ONLY these keys: "instruction", "input", "output".
    Return a JSON object: {{"cases": [{{ "instruction": "...", "input": "...", "output": "..." }}, ...]}}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a clinical BAMS doctor. You only provide Pure Vegetarian advice with precise measurements."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content).get("cases", [])
    except Exception as e:
        print(f"\n❌ Error generating {theme}: {e}")
        return []

# 2. Main Execution
output_file = "Samsara_2000_PureVeg_RealTime.jsonl"
total_goal = 2000
current_count = 0

print(f"🚀 Starting Real-Time Generation for {total_goal} Pure-Veg cases...")

with open(output_file, 'a', encoding='utf-8') as f:
    while current_count < total_goal:
        for theme in THEMES:
            for region in REGIONS:
                if current_count >= total_goal: break
                
                batch = generate_clinical_batch(5, theme, region)
                
                if not batch:
                    time.sleep(2) # Wait before retry
                    continue

                for case in batch:
                    if case.get("input") and case.get("output"):
                        # --- REAL-TIME VISUALIZATION ---
                        print(f"\n[CASE {current_count + 1}/{total_goal}]")
                        print(f"Region: {region} | Theme: {theme}")
                        # Print a snippet of the input so you see the profile being added
                        print(f"Profile: {str(case['input'])[:120]}...") 
                        
                        f.write(json.dumps(case) + "\n")
                        f.flush()  # Forces the case to be written to the file immediately
                        current_count += 1
                
                time.sleep(0.5) 

print(f"\n🏁 SUCCESS: {current_count} cases saved in {output_file}")