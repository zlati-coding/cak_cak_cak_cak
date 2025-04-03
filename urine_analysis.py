import ollama
import serial
import time
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to check if Ollama is running
def is_ollama_running():
    """Check if Ollama service is running."""
    try:
        result = subprocess.run(["pgrep", "-f", "ollama"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️ Error checking Ollama status: {e}")
        return False

# Function to wait for Ollama to start
def wait_for_ollama(timeout=60, interval=5):
    """Wait for Ollama to start, with a timeout."""
    elapsed_time = 0
    while not is_ollama_running():
        if elapsed_time >= timeout:
            print("❌ Ollama did not start within the timeout period. Exiting...")
            return False
        print(f"⏳ Waiting for Ollama to start... ({elapsed_time}/{timeout} sec)")
        time.sleep(interval)
        elapsed_time += interval
    print("✅ Ollama is now running. Proceeding with script execution.")
    return True

# Set up the serial connection
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

print("✅ Starting data collection...")
time.sleep(16)

# Collect raw data from serial input
raw_data_log = []
start_time = time.time()
while time.time() - start_time < 5:
    try:
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode('utf-8').strip()
            raw_data_log.append(raw_data)
            print(f"📩 Received: {raw_data}")
    except Exception as e:
        print("⚠️ Error reading from serial:", e)

# Parse raw data into structured format
urine_samples = []
current_sample = {}
for line in raw_data_log:
    if "PH value:" in line:
        current_sample["ph_value"] = float(line.split(": ")[1])
    elif "Clear urine with hex color:" in line:
        current_sample["hex_color"] = line.split(": ")[1]
        current_sample["is_clear"] = True
        urine_samples.append(current_sample)
        current_sample = {}  # Reset for next sample
    elif "urine with hex color:" in line:
        current_sample["hex_color"] = line.split(": ")[1]
        current_sample["is_clear"] = False
        urine_samples.append(current_sample)
        current_sample = {}  # Reset for next sample

# Calculate the average pH value
average_ph = sum(sample["ph_value"] for sample in urine_samples) / len(urine_samples)
# Determine if the majority of samples are clear
is_mostly_clear = sum(1 for sample in urine_samples if sample["is_clear"]) > (len(urine_samples) / 2)
# Use the most common hex color
most_common_color = max(set(sample["hex_color"] for sample in urine_samples), key=lambda c: sum(1 for s in urine_samples if s["hex_color"] == c))

# Reference values for normal urine
reference_ph_min = 4.5
reference_ph_max = 8.0
reference_clear = True  # Typically, healthy urine is clear
reference_colors = {"#FAFAD2", "#FFFFE0", "#FFFACD"}  # Light yellow shades

# Format data for AI prompt
raw_text_data = f"Average pH: {average_ph:.2f}, Most Common Color: {most_common_color}, Mostly Clear: {is_mostly_clear}"

# AI Analysis with Ollama
prompt = f"""
Analyze the following raw urine sensor data and provide insights:

{raw_text_data}

The data consists of:
- The color of the urine (in hex)
- The pH levels of the urine
- A boolean representing whether the urine is mostly clear or unclear

Please provide an accurate prediction about the provided data.
You have to tell possible health risks, and give an advice about possible diet change for example.
I don't want you to say things like "I can't precisely predict" or "I can't tell you have to visit a doctor.
"""

try:
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    ai_analysis = response["message"]["content"]
except Exception as e:
    print(f"❌ Error communicating with Ollama: {e}")
    exit(1)

# Print results
print("\n=== Raw Urine Sensor Data ===")
print(raw_text_data)

print("\n=== AI Analysis ===")
print(ai_analysis)

# Email setup
from_email = "cakcakurine@gmail.com"
to_email = "ikonomovdaniel2@gmail.com"
password = "ssipjnlhqhqcslmu"  # Use environment variables for security!

# Create the message
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "Urine Analysis Report from Raspberry Pi"

# Body of the email
body = f"""
Here is the urine analysis report:

Raw Data:
{raw_text_data}

Reference Values:
- Normal pH Range: {reference_ph_min} - {reference_ph_max}
  - Your pH Value: {average_ph:.2f} ({'Normal' if reference_ph_min <= average_ph <= reference_ph_max else 'Out of Range'})
- Healthy Urine Should Be Clear: {reference_clear}
  - Your Urine: {'Clear' if is_mostly_clear else 'Unclear'} ({'Normal' if is_mostly_clear == reference_clear else 'Potential Issue'})
- Healthy Urine Colors: {', '.join(reference_colors)}
  - Your Color: {most_common_color} ({'Normal' if most_common_color in reference_colors else 'Unusual'})

AI Analysis:
{ai_analysis}

If you have any further questions or symptoms, please consult a healthcare provider.
"""
msg.attach(MIMEText(body, 'plain'))

# Send the email
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Email sending failed: {e}")
finally:
    server.quit()
