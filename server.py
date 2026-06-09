from http.server import BaseHTTPRequestHandler
import json
import time

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # মোবাইল অ্যাপ থেকে আসা ডেটা পড়া
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            node_id = req_data.get("node_id", "UNKNOWN_NODE")
            status = req_data.get("status")
            
            # ইউজার যদি টাস্ক কমপ্লিট করে রিকোয়েস্ট পাঠায়
            if status == "COMPLETED":
                pay_rate = 0.0015 # প্রতি কাজের জন্য ১.৫ সেন্ট বা ১৫-২০ পয়সা
                
                # রেসপন্স ডাটা রেডি করা (বাস্তবে ডাটাবেজ আপডেট সাকসেস)
                response = {
                    "status": "SUCCESS",
                    "message": f"Added ${pay_rate} to {node_id}'s account.",
                    "added_balance": pay_rate,
                    "server_time": int(time.time())
                }
            else:
                # নতুন কাজের জন্য এআই টাস্ক প্যাকেট পাঠানো
                response = {
                    "status": "NEW_JOB",
                    "job_id": f"JOB_{int(time.time())}",
                    "task_type": "SENTIMENT_ANALYSIS",
                    "text_data": "This DeCent-AI platform is amazing and the best setup ever!"
                }
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))

    def do_GET(self):
        # সার্ভার লাইভ আছে কিনা চেক করার জন্য
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("🚀 DeCent-AI Vercel Master Server is LIVE!".encode('utf-8'))
