# CoderAgent Log - Attempt 1

## คำขอ: Enter your request for [Coder]: เขียนฟังก์ชัน Python ที่คำนวณ factorial และต้อง raise ValueError ถ้า input เป็นลบ

### โค้ดที่สร้างโดย CoderAgent
```python
def factorial(n):
    if n < 0:
        raise ValueError("Input must be non-negative")
    elif n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
```

### ผลการประเมินโค้ด
**รันสำเร็จ:** True
**ข้อความ:** ไม่สามารถสร้าง Test Cases ที่ถูกต้องได้
โค้ดมี Syntax ถูกต้องเบื้องต้น.

**รายละเอียด Test Results:**
ไม่มีรายละเอียด Test Results (อาจเกิดข้อผิดพลาดในการสร้าง/parse Test Cases หรือไม่มี Test Cases)

**บันทึกเมื่อ:** 20250622_202731
