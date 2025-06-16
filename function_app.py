import azure.functions as func
import logging
import os
import google.generativeai as genai

# ตั้งค่าแอปฟังก์ชัน
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# ดึง API Key จากการตั้งค่าของ Function App
GEMINI_API_KEY = os.environ.get('AIzaSyAdAQhJd0-paOJTDJZpmTuLQT6JWyz88MA')

# ตรวจสอบว่ามี API Key หรือไม่ก่อนที่จะ configure
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
else:
    model = None # ถ้าไม่มี Key ให้ model เป็น None

@app.route(route="ask") # เปลี่ยน route เป็น ask เพื่อความชัดเจน
def ask_gemini_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a new request.')

    # ตรวจสอบว่า model พร้อมใช้งานหรือไม่ (มี API Key หรือไม่)
    if not model:
        return func.HttpResponse("ERROR: Gemini API key is not configured.", status_code=500)

    prompt = req.params.get('prompt')
    if not prompt:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            prompt = req_body.get('prompt')

    if prompt:
        try:
            # ส่ง prompt ไปให้ Gemini และรอคำตอบ
            response = model.generate_content(prompt)

            # ส่งคำตอบที่ได้จาก Gemini กลับไปให้ผู้ใช้
            return func.HttpResponse(response.text, status_code=200, mimetype="text/plain; charset=utf-8")

        except Exception as e:
            return func.HttpResponse(f"Error calling Gemini API: {str(e)}", status_code=500)
    else:
        return func.HttpResponse(
             "This function connects to Gemini. Pass a 'prompt' in the query string to ask a question.",
             status_code=200
        )