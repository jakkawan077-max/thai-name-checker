import streamlit as st
import requests

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ส่องชื่อไทย - วิเคราะห์ภาษาสันสกฤต", page_icon="🔮")

def analyze_name(name, token):
    # ใช้โมเดลภาษาไทย/อังกฤษที่เก่งๆ บน Hugging Face
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {token}"}
    
    prompt = f"Analyze the Thai name '{name}'. Is it from Sanskrit? What does it mean? Answer in Thai briefly and beautifully."
    
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]['generated_text'].split(prompt)[-1]
    else:
        return "ขออภัย ระบบขัดข้องชั่วคราว ลองใหม่อีกครั้งนะครับ"

# UI หน้าเว็บ
st.title("🔮 วิเคราะห์รากศัพท์ชื่อไทย")
st.subheader("ชื่อของคุณเป็นภาษาสันสกฤตหรือไม่? ให้ AI ช่วยบอก!")

name = st.text_input("กรอกชื่อของคุณ (ไม่ต้องมีนามสกุล):", placeholder="เช่น อนันดา, ปรียา")

if st.button("วิเคราะห์ชื่อ"):
    if name:
        with st.spinner('กำลังค้นหาตำรา...'):
            # ดึง Token จาก Secrets ของ Streamlit
            result = analyze_name(name, st.secrets["HF_TOKEN"])
            
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #764ba2;">
                <h4>ผลการวิเคราะห์ชื่อ: {name}</h4>
                <p>{result}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # ปุ่ม Facebook Share
            share_url = f"https://www.facebook.com/sharer/sharer.php?u=https://share.streamlit.io/&quote=ชื่อ {name} ของฉันแปลว่าอะไร? มาลองเช็คกันที่นี่!"
            st.markdown(f'<br><a href="{share_url}" target="_blank"><button style="background-color:#1877F2; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">แชร์ลง Facebook</button></a>', unsafe_allow_html=True)
    else:
        st.warning("กรุณากรอกชื่อก่อนกดปุ่มครับ")
