import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

THEMES = [
    "PCOS & Hormonal Imbalance", "Thyroid (Hypo/Hyper)", "Weight Loss (Kapha reduction)",
    "Weight Gain (Vata nourishing)", "Digestive Health (Acidity/IBS)", 
    "Modern Lifestyle Stress & Burnout", "Skin/Hair Health (Pitta/Acidity)", 
    "Postpartum & Women's Strength", "Sedentary Professional (Cervical/Stress)"
]

def generate_sft_batch(batch_size=20, theme="General Health"):
    """
    Generates clinical training cases in JSON format.
    Includes all 13 required parameters for accurate diet generation.
    """
    system_prompt = f"""
    You are a BAMS (Ayurveda) Doctor. Generate {batch_size} unique training cases in JSON format.
    Focus Theme: {theme}
    
    Each case MUST incorporate these 13 parameters:
    1. Age, 2. Gender, 3. Weight, 4. Height, 5. BMI, 
    6. Goals (Condition-specific), 7. Symptoms, 
    8. Cycle details (if female), 9. Lifestyle (Step count/Exercise), 
    10. Food habits (Timings/Veg type), 11. Dosha (Prakriti & Vikriti), 
    12. Pre-existing issues, 13. Stress/Mood.
    
    The 'doctor_response' MUST include:
    - Clinical Reasoning: Analyze Agni, Dosha imbalance, and Dhatu involvement.
    - Diet Plan: Morning, Lunch, and Dinner (Regional Pure Veg).
    - Safety: Exercise limits and clinical red-flags.
    """

    user_prompt = f"Generate a JSON object with a key 'cases' containing {batch_size} unique training examples for {theme}."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content).get("cases", [])
    except Exception as e:
        print(f"Error in {theme} batch: {e}")
        return []

#  Main Execution
output_file = "Samsara_1000_Cases_Diet.jsonl"
total_goal = 1000
current_count = 0

print(f"🚀 Starting generation of {total_goal} cases for Samsara...")

with open(output_file, 'w', encoding='utf-8') as f:
    while current_count < total_goal:
        for theme in THEMES:
            if current_count >= total_goal: break
            
           
            batch = generate_sft_batch(10, theme)
            for case in batch:
                training_row = {
                    "instruction": "You are a clinical Ayurveda assistant. Analyze the user's data and provide a personalized diet plan.",
                    "input": str(case.get("user_profile", "")),
                    "output": str(case.get("doctor_response", ""))
                }
                f.write(json.dumps(training_row) + "\n")
                current_count += 1
            
            print(f"Progress: {current_count}/{total_goal} | Theme: {theme}")
            time.sleep(1) # Prevent rate limits

print(f"🏁 SUCCESS: 1000 cases saved in {output_file}")