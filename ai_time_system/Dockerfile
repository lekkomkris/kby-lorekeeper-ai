# Dockerfile

# ใช้ Python 3.11 Slim เป็น Base Image เพื่อให้ Image มีขนาดเล็ก
FROM python:3.11-slim

# กำหนด Working Directory ภายใน Container เป็น /app
WORKDIR /app

# Copy ไฟล์ requirements.txt เข้าไปใน Container
# แล้วติดตั้ง Python dependencies ทั้งหมดที่อยู่ใน requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ไฟล์ realtime_clock.py เข้าไปใน Working Directory (/app)
COPY realtime_clock.py .

# กำหนด Command ที่จะรันเมื่อ Container เริ่มต้นทำงาน
# ซึ่งคือการรันสคริปต์ Python realtime_clock.py
CMD ["python", "realtime_clock.py"]