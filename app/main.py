from scapy.all import sniff, IP, TCP
import mysql.connector
from pyfiglet import Figlet
from tqdm import tqdm
import time

# define
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="ymp"
)

mycursor = mydb.cursor()

if mydb.is_connected():
    print("CONNECT!")

    mycursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            log_message TEXT NOT NULL,
            log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_src VARCHAR(45),
            tcp_sport INT,
            ip_dst VARCHAR(45),
            tcp_dport INT,
            severity VARCHAR(10)
        );
        """
    )

# logging.basicConfig(filename='logs.txt', level=logging.INFO)

def banner():
    f = Figlet()
    print(f.renderText("Threats_Detector"))
    print("~# Author: PT. Yuk Mari Proyek Indonesia")
    print("~# Copyright © 2025")

def load_payloads(filepath, desc):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        payloads = []
        for line in tqdm(lines, desc=desc, total=len(lines)):
            payloads.append(r"{}".format(line.strip()))
            # time.sleep(0.001337)
    return payloads

sqli_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/sqli_attack.txt', "Loading SQLi Payload")
xss_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/xss_attack.txt', "Loading XSS Payload")
csv_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/csv_attack.txt', "Loading CSV Payload")
command_injection_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/command_injection_attack.txt', "Loading Command Injection Payload")
directory_traversal_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/directory_traversal_attack.txt', "Loading Directory Traversal Payload")
file_inclusion_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/file_inclusion_attack.txt', "Loading File Inclusion Payload")
nosql_injection_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/nosql_attack.txt', "Loading NoSQL Injection Payload")
xml_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/xml_attack.txt', "Loading XML Payload")
ssii_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/ssii_attack.txt', "Loading SSI Payload")
ssti_payloads = load_payloads('C:/Users/alfiy/OneDrive/Desktop/IDS/magang-alfian/app/static/payload/ssti_attack.txt', "Loading SSTI Payload")

def detect_payload(input_payload, attack_payloads):
    
    for payload in attack_payloads:
        if payload in input_payload:
            return payload
    
    return None

payload_types = [
    ('SQL Injection', sqli_payloads, 'CRITICAL'),
    ('XSS Injection', xss_payloads, 'MEDIUM'),
    ('XML Injection', xml_payloads, 'HIGH'),
    ('NoSQL Injection', nosql_injection_payloads, 'CRITICAL'),
    ('File Inclusion', file_inclusion_payloads, 'MEDIUM'),
    ('CSV Injection', csv_payloads, 'MEDIUM'),
    ('Directory Traversal', directory_traversal_payloads, 'MEDIUM'),
    ('SST Injection', ssti_payloads, 'HIGH'),
    ('SSI Injection', ssii_payloads, 'HIGH'),
    ('Command Injection', command_injection_payloads, 'HIGH')
        ]

def analyze_packet(packet):
    if IP in packet and TCP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        tcp_sport = packet[TCP].sport
        tcp_dport = packet[TCP].dport

        try:
            payload = bytes(packet[TCP].payload).decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            return

        # Comprehensive payload match checking
        for attack_type, attack_payloads, severity in payload_types:
            detected_payload = detect_payload(payload, attack_payloads)
            if detected_payload:
                log_msg = f"{attack_type} Attack Detected! Payload: {detected_payload}"
                print(log_msg)
                
                # Log attack details to database with specified severity
                sql = "INSERT INTO logs (log_message, ip_src, tcp_sport, ip_dst, tcp_dport, severity) VALUES (%s, %s, %s, %s, %s, %s)"
                mycursor.execute(sql, (log_msg, ip_src, tcp_sport, ip_dst, tcp_dport, severity))
                mydb.commit()

if __name__ == '__main__':
    banner()
    print("Server is running...")
    sniff(prn=analyze_packet)