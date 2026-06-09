import socket
import threading
import json
import sqlite3
import time
import os

# ১. ডাটাবেজ সেটআপ (ইউজার ব্যালেন্স ও টাস্ক ট্র্যাক করার জন্য)
def init_db():
    conn = sqlite3.connect('decent_ai.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            node_id TEXT PRIMARY KEY,
            balance REAL DEFAULT 0.0,
            tasks_completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def update_user_balance(node_id, amount):
    conn = sqlite3.connect('decent_ai.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (node_id, balance, tasks_completed) VALUES (?, 0.0, 0)", (node_id,))
    cursor.execute("UPDATE users SET balance = balance + ?, tasks_completed = tasks_completed + 1 WHERE node_id = ?", (amount, node_id))
    conn.commit()
    conn.close()

def handle_node(client_socket, client_address):
    print(f"📡 New Edge Node Connected: {client_address}")
    try:
        job_packet = {
            "job_id": f"JOB_{int(time.time())}",
            "task_type": "SENTIMENT_ANALYSIS",
            "text_data": "This DeCent-AI platform is amazing and the best setup ever!"
        }
        client_socket.sendall(json.dumps(job_packet).encode('utf-8'))
        
        raw_response = client_socket.recv(2048).decode('utf-8')
        if raw_response:
            result = json.loads(raw_response)
            if result.get("status") == "COMPLETED":
                node_id = f"NODE_{client_address[1]}"
                pay_rate = 0.0015
                update_user_balance(node_id, pay_rate)
                print(f"💰 Success! {node_id} earned ${pay_rate}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client_socket.close()

def start_master_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # রেন্ডার ক্লাউডের পোর্ট ধরার জন্য os.environ ব্যবহার করা হয়েছে
    port = int(os.environ.get("PORT", 7777))
    server.bind(('0.0.0.0', port)) 
    server.listen(5)
    print(f"🚀 DeCent-AI Master Cloud Server is LIVE on port {port}...")
    
    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_node, args=(client_socket, client_address), daemon=True).start()

if __name__ == '__main__':
    start_master_server()
