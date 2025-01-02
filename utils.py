import os
import re
from dotenv import load_dotenv

def load_env():
    """Muhit o‘zgaruvchilarini yuklash uchun."""
    load_dotenv()

def preprocess_message(message):
    """
    Guruhdan kelgan xabarlarni qayta ishlash.
    """
    # IP-manzilni aniqlash
    ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    ip_match = re.search(ip_pattern, message)
    ip = ip_match.group(0) if ip_match else "0.0.0.0"

    # Port raqamlarini aniqlash
    port_pattern = r"\b\d{1,5}\b"
    ports = re.findall(port_pattern, message)
    source_port = ports[0] if ports else 0
    dest_port = ports[1] if len(ports) > 1 else 0

    # Ma'lumotni tayyorlash
    return {
        "ip.src": ip,
        "tcp.srcport": source_port,
        "tcp.dstport": dest_port,
        # Boshqa kerakli ustunlarni qo'shing
    }
