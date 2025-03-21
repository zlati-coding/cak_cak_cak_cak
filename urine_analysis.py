import ollama
import serial
import time
import re

# **Set up the serial connection**
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

print("✅ Starting data collection...")

# **Collect 5 seconds of raw data**
raw_data_log = []
start_time = time.time()

# Collect for 5 seconds and then stop
while time.time() - start_time < 5:
    try:
        if ser.in_waiting > 0:  # Check if data is available
            raw_data = ser.readline().decode('utf-8').strip()
            raw_data_log.append(raw_data)
            print(f"📩 Received: {raw_data}")
    except Exception as e:
        print("⚠️ Error reading from serial:", e)

# **Format raw data for AI**
raw_text_data = "\n".join(raw_data_log)

# **AI Analysis with Ollama**
prompt = f"""
Analyze the following raw urine sensor data and provide insights:

{raw_text_data}

The data consists of:
- Urine color (HEX codes)
- Ambient light levels (lux)

Please provide insights on potential health conditions based on this information.
"""

response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

# **Print results**
print("\n=== Raw Urine Sensor Data ===")
print(raw_text_data)

print("\n=== AI Analysis ===")
print(response["message"]["content"])

# **Ask for additional symptoms**
user_symptoms = input("\nDo you have any symptoms? (e.g., dark urine, frequent urination, fatigue): ").strip()

if user_symptoms:
    prompt_with_symptoms = f"""
    Given the raw urine sensor data:

    {raw_text_data}

    And considering the following patient symptoms: "{user_symptoms}", analyze the results and provide a diagnosis.
    """

    response_symptoms = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt_with_symptoms}])

    print("\n=== Updated AI Analysis Based on Symptoms ===")
    print(response_symptoms["message"]["content"])
else:
    print("\nNo additional symptoms provided. AI analysis remains based on urine data only.")
