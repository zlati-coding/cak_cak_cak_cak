import pandas as pd
import ollama

# Simulated urine sensor data
data = [
    {"timestamp": "2025-03-20 12:00", "ph": 6.5, "glucose": 0, "protein": 1, "ketones": 0, "nitrites": 1},
    {"timestamp": "2025-03-20 12:05", "ph": 5.8, "glucose": 2, "protein": 0, "ketones": 1, "nitrites": 0},
    {"timestamp": "2025-03-20 12:10", "ph": 7.2, "glucose": 0, "protein": 2, "ketones": 0, "nitrites": 1},
    {"timestamp": "2025-03-20 12:15", "ph": 6.0, "glucose": 3, "protein": 1, "ketones": 2, "nitrites": 0},
    {"timestamp": "2025-03-20 12:20", "ph": 6.8, "glucose": 0, "protein": 0, "ketones": 0, "nitrites": 1},
]

# Convert to DataFrame
df = pd.DataFrame(data)
df["timestamp"] = pd.to_datetime(df["timestamp"])  # Convert timestamp to datetime

# Summarize the data
data_summary = df.describe().to_string()

# AI Analysis with Ollama - Initial Report
prompt = f"""
Analyze the following urine sensor data and detect potential health issues:

{data_summary}

Provide insights in simple language, explaining any abnormal readings.
"""

# Use the correct Ollama API without explicitly setting the base URL
response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

# Print initial AI analysis
print("\n=== Urine Sensor Data ===")
print(df)
print("\n=== AI Analysis ===")
print(response["message"]["content"])

# Ask the user for additional symptoms
user_symptoms = input("\nDo you have any symptoms? (e.g., pain in kidneys, frequent urination, fatigue): ").strip()

if user_symptoms:
    # AI Analysis with symptoms
    prompt_with_symptoms = f"""
    Given the urine sensor data:

    {data_summary}

    And considering the following patient symptoms: "{user_symptoms}", analyze the results again and provide a more accurate diagnosis.
    """

    response_symptoms = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt_with_symptoms}])

    print("\n=== Updated AI Analysis Based on Symptoms ===")
    print(response_symptoms["message"]["content"])
else:
    print("\nNo additional symptoms provided. AI analysis remains based on urine data only.")
import pandas as pd
import ollama

# Simulated urine sensor data
data = [
    {"timestamp": "2025-03-20 12:00", "ph": 6.5, "glucose": 0, "protein": 1, "ketones": 0, "nitrites": 1},
    {"timestamp": "2025-03-20 12:05", "ph": 5.8, "glucose": 2, "protein": 0, "ketones": 1, "nitrites": 0},
    {"timestamp": "2025-03-20 12:10", "ph": 7.2, "glucose": 0, "protein": 2, "ketones": 0, "nitrites": 1},
    {"timestamp": "2025-03-20 12:15", "ph": 6.0, "glucose": 3, "protein": 1, "ketones": 2, "nitrites": 0},
    {"timestamp": "2025-03-20 12:20", "ph": 6.8, "glucose": 0, "protein": 0, "ketones": 0, "nitrites": 1},
]

# Convert to DataFrame
df = pd.DataFrame(data)
df["timestamp"] = pd.to_datetime(df["timestamp"])  # Convert timestamp to datetime

# Summarize the data
data_summary = df.describe().to_string()

# AI Analysis with Ollama - Initial Report
prompt = f"""
Analyze the following urine sensor data and detect potential health issues:

{data_summary}

Provide insights in simple language, explaining any abnormal readings.
"""

# Use the correct Ollama API without explicitly setting the base URL
response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

# Print initial AI analysis
print("\n=== Urine Sensor Data ===")
print(df)
print("\n=== AI Analysis ===")
print(response["message"]["content"])

# Ask the user for additional symptoms
user_symptoms = input("\nDo you have any symptoms? (e.g., pain in kidneys, frequent urination, fatigue): ").strip()

if user_symptoms:
    # AI Analysis with symptoms
    prompt_with_symptoms = f"""
    Given the urine sensor data:

    {data_summary}

    And considering the following patient symptoms: "{user_symptoms}", analyze the results again and provide a more accurate diagnosis.
    """

    response_symptoms = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt_with_symptoms}])

    print("\n=== Updated AI Analysis Based on Symptoms ===")
    print(response_symptoms["message"]["content"])
else:
    print("\nNo additional symptoms provided. AI analysis remains based on urine data only.")
