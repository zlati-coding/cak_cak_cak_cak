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

# **Wait for Ollama before running main logic**
if not wait_for_ollama():
    exit(1)  # Exit script if Ollama fails to start

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
- The color of the urine (in hex)
- The pH levels of the urine
- A string which is "clear" or "unclear", that represents if the urine is clear and watery or unclear

Please provide an accurate prediction about the provided data.
You have to tell possible health risks, and give an advice about possible diet change for example.
The data samples are multiple, because I collected 5 seconds of the data.
I don't want you to say things like "I can't precisely predict" or "I can't tell you have to visit a doctor".
"""

try:
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    ai_analysis = response["message"]["content"]
except Exception as e:
    print(f"❌ Error communicating with Ollama: {e}")
    exit(1)

# **Print results**
print("\n=== Raw Urine Sensor Data ===")
print(raw_text_data)

print("\n=== AI Analysis ===")
print(ai_analysis)

# **Email setup**
from_email = "cakcakurine@gmail.com"
to_email = "ikonomovdaniel2@gmail.com"
password = "ssipjnlhqhqcslmu"  # Consider using environment variables for security!

# Create the message
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "Urine Analysis Report from Raspberry Pi"

# Body of the email with the AI analysis
body = f"""
Here is the urine analysis report:

Raw Data:
{raw_text_data}

AI Analysis:
{ai_analysis}

If you have any further questions or symptoms, please consult a healthcare provider.
"""
msg.attach(MIMEText(body, 'plain'))

# Send the email using Gmail's SMTP server
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Encrypt the connection
    server.login(from_email, password)  # Login to the server
    text = msg.as_string()  # Convert the message to a string format
    server.sendmail(from_email, to_email, text)  # Send the email
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Email sending failed: {e}")
finally:
    server.quit()  # Close the connection