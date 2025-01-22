import re
import logging
from scapy.all import sniff, IP, TCP

logging.basicConfig(filename='ids_log.txt', level=logging.INFO)

def title():
    print(r"|\====================================================/|")
    print(r"|    PNgendus Detector - Intrusion Detection System    |")
    print(r"|          Author: Yuk Mari Project  Indonesia         |")
    print(r"|                  Copyright © 2024/2025               |")
    print(r"|/====================================================\|")

def detect_xss(data):

    xss_patterns = [
        r"<script>", 
        r"</script>", 
        r"on[a-z]+=", 
        r"javascript:", 
        r"vbscript:", 
        r"expression", 
        r"onerror", 
        r"onconfirm" 
    ]

    for pattern in xss_patterns:
        if re.search(pattern, data, re.IGNORECASE):
            return True
        
    return False

def analyze_packet(packet):

    try:
        if IP in packet and TCP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport

            try:
                payload = bytes(packet[TCP].payload).decode('utf-8', errors='ignore') 
            except UnicodeDecodeError:
                payload = "Error to decode payload!"

            if detect_xss(payload):
                log_msg = f"Possible XSS attack detected: {ip_src}:{tcp_sport} -> {ip_dst}:{tcp_dport}"
                payload = f"Payload: {payload}"
                full_log = log_msg + '\n' + payload
                
                print (full_log)

                logging.info(full_log)

                return True

    except Exception as e:
        print(f"Error analyzing packets ==> {e}")

    return 'No Suspicious Activity Detected!'

if __name__ == '__main__':
    title()
    sniff(prn=analyze_packet)