import imaplib
import email
import smtplib
from email.mime.text import MIMEText

# IMAP settings (internet messaging access protocol)
IMAP_HOST = 'outlook.office365.com'
IMAP_PORT = 993
IMAP_USERNAME = 'pritishpawar15@outlook.com'
IMAP_PASSWORD = 'pawarramesh91567'

# SMTP settings (simple mail transfer protocol)
SMTP_HOST = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USERNAME = 'pritishpawar15@outlook.com'
SMTP_PASSWORD = 'pawarramesh91567'

# Connect to the IMAP server (internet messaging access protocol)
imap_server = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT) #IMAP4, uses clear text sockets; IMAP4_SSL uses encrypted communication over SSL sockets
imap_server.login(IMAP_USERNAME, IMAP_PASSWORD)
imap_server.select()

def get_sender_name(email_message):
    sender_name = email.utils.parseaddr(email_message['From'])[0]
    return sender_name

# Search for unread messages
status, data = imap_server.search(None, '(UNSEEN)')
if status == 'OK':
    for num in data[0].split():
        # Fetch the email message
        status, message_data = imap_server.fetch(num, '(RFC822)')
        if status == 'OK':
            raw_email = message_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # Get the sender's name
            sender_name = get_sender_name(email_message)
            
            # Print the sender's name
            print("Sender's Name:", sender_name)

            # Get the sender's email address
            sender_email = email.utils.parseaddr(email_message['From'])[1]
            
            # Print the sender's email address
            print("Sender's Email:", sender_email)
            
            # Create a reply email
            reply_subject = 'Re: ' + email_message['Subject']
            reply_text = f"Dear {sender_name},\n\nThank you for reaching out to us regarding your tech support query. We appreciate the opportunity to assist you.\nYour query has been registered and we would get back to you shrortly.\n\nBest regards,\nCafeXpress\nsupport@cafexpress.io"
            reply_email = MIMEText(reply_text)
            reply_email['Subject'] = reply_subject
            reply_email['From'] = SMTP_USERNAME
            reply_email['To'] = sender_email
            
            # Send the reply email
            smtp_server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            smtp_server.starttls()
            smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp_server.sendmail(SMTP_USERNAME, sender_email, reply_email.as_string())
            smtp_server.quit()

# Close the IMAP connection
imap_server.close()
imap_server.logout()
