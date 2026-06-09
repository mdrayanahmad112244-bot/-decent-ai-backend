from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            req_json = json.loads(post_data.decode('utf-8'))
            status = req_json.get("status")
            node_id = req_json.get("node_id", "UNKNOWN_NODE")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            if status == "FETCH_JOB":
                # মোবাইল অ্যাপে কাজ পাঠানোর রেসপন্স
                response_data = {
                    "status": "NEW_JOB",
                    "job_id": "JOB_BR_99",
                    "task_type": "AI_TEXT_ANALYSIS",
                    "text_data": "Processing distributed AI models for edge rendering networks.",
                    "added_balance": 0.0015
                }
            elif status == "COMPLETED":
                # কাজ শেষ হলে ব্যালেন্স অ্যাড করার কনফার্মেশন
                response_data = {
                    "status": "SUCCESS",
                    "node_id": node_id,
                    "added_balance": 0.0015,
                    "msg": "Balance sync completed successfully."
                }
            else:
                response_data = {"status": "INVALID_STATUS"}
                
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

