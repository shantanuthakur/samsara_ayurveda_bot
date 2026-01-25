import os
import json
import csv
import time
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


CATEGORIES = {
    "Women's Health (PCOS/Thyroid/PMS)": 60,
    "Metabolic (Weight/Diabetes/BP)": 50,
    "Digestion (Agni/IBS/Acidity)": 40,
    "Skin & Hair (Pitta/Detox)": 30,
    "Modern Lifestyle (Stress/Sleep/Corporate Burnout)": 40,
    "Dosha Logic (Prakriti/Vikriti/Seasons)": 30
}

def generate_doctor_qna(category, batch_count):
    """Generates a batch of professional Ayurvedic doctor Q&A pairs."""
    print(f"Generating {batch_count} questions for: {category}")
    
    prompt = f"""
    Act as a Senior BAMS Doctor. Generate {batch_count} unique, high-quality Q&A pairs for the {category} category.
    
    Each pair must include:
    1. 'Question': A common or complex patient query.
    2. 'Answer': A professional clinical response explaining the root cause (Dosha/Agni/Ama) and the Ayurvedic solution.
    
    Format the output strictly as a JSON object with a 'qna_list' key containing objects with 'category', 'question', and 'answer'.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a clinical Ayurvedic data architect."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content).get("qna_list", [])
    except Exception as e:
        print(f"Error in batch: {e}")
        return []


master_qna = []
output_file = "Doctor_QnA_250_Master.csv"

for category, target_count in CATEGORIES.items():
    
    for i in range(0, target_count, 10):
        batch = generate_doctor_qna(category, 10)
        master_qna.extend(batch)
        time.sleep(1) 

if master_qna:
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["category", "question", "answer"])
        writer.writeheader()
        writer.writerows(master_qna)
    print(f"Success! 250 Questions saved to {output_file}")