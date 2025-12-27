import streamlit as st
import requests

# บังคับให้หน้าเว็บเป็น Light Mode เสมอเพื่อป้องกันฟอนต์สีขาวมองไม่เห็น
st.set_page_config(page_title="ส่องชื่อไทย", page_icon="🔮", layout="centered")

# CSS สำหรับตกแต่ง (บังคับสีฟอนต์เป็นสีดำ/เทาเข้ม)
st.markdown("""
    <style>
    .reportview-container .main .block-container { color: #1f1f1f; }
    h1, h2, h3, h4, p, span, div { color: #1f1f1f !important; }
    .stButton>button { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white !important; 
        border-radius: 10px;
        width: 100%;
    }
    .result-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #764ba2;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def analyze_name(name, token):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {token}"}
    
    # ปรับ Prompt ให้ AI ตอบเป็นโครงสร้างที่ชัดเจน
    prompt = f"<s>[INST] วิเคราะห์ชื่อไทย: '{name}' ว่ามีรากศัพท์จากภาษาสันสกฤตไหม? แปลว่าอะไร ตอบเป็นภาษาไทยสั้นๆ ไม่เกิน 3 บรรทัด [/INST]</s>"
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=10)
        if response.status_code == 200:
            raw_text = response.json()[0]['generated_text']
            return raw_text.split("[/INST]")[-1].strip()
        else:
            return "ขออภัย AI กำลังพักผ่อน (Overloaded) กรุณาลองใหม่ในอีก 1 นาทีครับ"
    except Exception as e:
        return f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}"

# UI
st.title("🔮 ส่องชื่อไทย")
st.write("ตรวจสอบรากศัพท์สันสกฤตและความหมายของชื่อคุณ")

name = st.text_input("กรอกชื่อของคุณ:", placeholder="เช่น อนันดา, ปรียา")

if st.button("วิเคราะห์เลย"):
    if name:
        with st.spinner('AI กำลังอ่านตำรา...'):
            # ดึง Token จาก Secrets
            hf_token = st.secrets["HF_TOKEN"]
            result = analyze_name(name, hf_token)
            
            # แสดงผลในกล่องที่ตกแต่งแล้ว
            st.markdown(f"""
            <div class="result-box">
                <h3 style="margin-top:0;">ชื่อ: {name}</h3>
                <p>{result}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # ปุ่ม Facebook Share
            share_text = f"ชื่อ {name} ของฉันมีความหมายว่า... {result[:50]}..."
            share_url = f"https://www.facebook.com/sharer/sharer.php?u=https://share.streamlit.io/&quote={share_text}"
            st.markdown(f'<br><a href="{share_url}" target="_blank"><button style="background-color:#1877F2; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; width:100%;">แชร์ผลลัพธ์ลง Facebook</button></a>', unsafe_allow_html=True)
    else:
        st.warning("กรุณากรอกชื่อก่อนครับ")
