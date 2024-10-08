import os
import smtplib
import difflib
import requests
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import psutil

# Function to get all MAC addresses from network interfaces
def get_mac_addresses():
    mac_addresses = {}
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:  # AF_LINK corresponds to MAC address
                mac_addresses[interface] = addr.address
    return mac_addresses

# Function to send an email with the differences and MAC addresses
def send_email(differences, mac_addresses):
    from_email = "jasonereso.nextvas@gmail.com"
    to_emails = ["jasonereso.nextvas@gmail.com", "j.ereso157@gmail.com", "eric.nextvas@gmail.com", "heldrixnabor4@gmail.com", "el3c.joseph@gmail.com"]
    subject = "Hosts File Difference Detected"
    
    mac_addresses_str = "<br>".join([f"{interface}: {mac}" for interface, mac in mac_addresses.items()])

    body = f"""
    <html>
    <body>
        <h2 style="color: #4CAF50;">Hosts File Difference Detected</h2>
        <p><strong>MAC Addresses:</strong></p>
        <p>{mac_addresses_str}</p>
        <p><strong>Differences in Hosts File:</strong></p>
        <pre style="background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd; font-size: 14px;">
            {differences}
        </pre>
        <p>This email was automatically generated by the system.</p>
    </body>
    </html>
    """

    # MIME Multipart for HTML email
    msg = MIMEMultipart("alternative")
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    
    part1 = MIMEText(body, 'html')
    msg.attach(part1)

    # Send the email using Gmail's SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(from_email, "yfto iyiq xfpl uqis")
    text = msg.as_string()
    smtp_server.sendmail(from_email, to_emails, text)
    smtp_server.quit()

# Function to read the local hosts file
def read_local_hosts():
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    with open(hosts_path, 'r') as file:
        return file.readlines()

# Function to fetch the remote hosts file from GitHub
def fetch_remote_hosts():
    url = "https://raw.githubusercontent.com/ITJason-nextvas/host/main/host.txt"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        raise Exception(f"Failed to fetch the file: {response.status_code}")

# Function to compare the local and remote hosts file
def compare_hosts(local_hosts, remote_hosts):
    differences = list(difflib.unified_diff(local_hosts, remote_hosts, lineterm=''))
    return "\n".join(differences) if differences else None

def main():
    try:
        # Read local hosts file
        local_hosts = read_local_hosts()

        # Fetch remote hosts file
        remote_hosts = fetch_remote_hosts()

        # Compare files
        differences = compare_hosts(local_hosts, remote_hosts)

        # If there are differences, send an email
        if differences:
            mac_addresses = get_mac_addresses()  # Get all MAC addresses
            send_email(differences, mac_addresses)  # Send email with differences and all MACs
            print("Differences found and email sent.")
        else:
            print("No differences found.")

    except Exception as e:
        print(f"Error asdasdas : {e}")

if __name__ == "__main__":
    main()
