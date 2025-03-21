import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email setup
from_email = "cakcakurine@gmail.com"
to_email = "ikonomovdaniel2@gmail.com"
password = "ssipjnlhqhqcslmu"  # If using Gmail, you should create an app-specific password for better security.

# Create the message
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = "Test Email from Raspberry Pi"

# Body of the email
body = "This is a test email sent from Raspberry Pi!"
msg.attach(MIMEText(body, 'plain'))

# Send the email using Gmail's SMTP server
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Encrypt the connection
    server.login(from_email, password)  # Login to the server
    text = msg.as_string()  # Convert the message to a string format
    server.sendmail(from_email, to_email, text)  # Send the email
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    server.quit()  # Close the connection
