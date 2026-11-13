import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Hospital Token System", page_icon="🏥", layout="centered")

if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_token" not in st.session_state:
    st.session_state.current_token = 0

st.title("🏥 City Hospital - Live Token System")
st.caption("WhatsApp + Call + Walk-in Hybrid Queue Demo")

tab1, tab2, tab3 = st.tabs(["📱 WhatsApp Booking (Test)", "🖥️ Reception (Call/Walk-in)", "🩺 Doctor Screen"])

with tab1:
    st.subheader("WhatsApp Auto-Reply Simulator")
    st.info("Patient hospital ke WhatsApp par 'Book' likh kar details bhejega:")
    
    w_name = st.text_input("Patient ka Naam (WhatsApp):", placeholder="Jaise: Rahul Sharma")
    w_age = st.number_input("Umar (Age):", min_value=1, max_value=120, value=25)
    w_phone = st.text_input("WhatsApp Number:", placeholder="9876543210")
    
    if st.button("Send WhatsApp Message 📩"):
        if w_name:
            token_no = len(st.session_state.queue) + 1
            st.session_state.queue.append({
                "Token": f"#{token_no:02d}",
                "Name": w_name,
                "Age": w_age,
                "Source": "WhatsApp 📱",
                "Status": "Waiting",
                "Time": datetime.now().strftime("%I:%M %p")
            })
            st.success(f"🤖 **AI Auto-Reply Sent to {w_name}:**\n\nNamaste {w_name}! Aapka appointment book ho gaya hai. Aapka Token Number **#{token_no:02d}** hai. Kripya samay par clinic pahunchen.")
        else:
            st.warning("Kripya patient ka naam likhein!")

with tab2:
    st.subheader("Reception Counter (Call ya Bina Phone Wale)")
    r_name = st.text_input("Patient ka Naam (Offline):", placeholder="Jaise: Sunita Devi")
    r_age = st.number_input("Patient Umar:", min_value=1, max_value=120, value=40)
    r_type = st.selectbox("Booking Mode:", ["Phone Call 📞", "Walk-in (Counter) 🚶"])
    
    if st.button("Generate Token Parchi 🎟️"):
        if r_name:
            token_no = len(st.session_state.queue) + 1
            st.session_state.queue.append({
                "Token": f"#{token_no:02d}",
                "Name": r_name,
                "Age": r_age,
                "Source": r_type,
                "Status": "Waiting",
                "Time": datetime.now().strftime("%I:%M %p")
            })
            st.success(f"✅ Token **#{token_no:02d}** generate ho gaya hai ({r_name} - {r_type})")
        else:
            st.warning("Kripya patient ka naam dalein!")

with tab3:
    st.subheader("Doctor Cabin Live Control")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Abhi Andar Hain (Current Token)", f"#{st.session_state.current_token:02d}")
    with col2:
        st.metric("Total Patients Today", len(st.session_state.queue))
        
    if st.button("➡️ Next Patient Bulayein", type="primary"):
        if st.session_state.current_token < len(st.session_state.queue):
            if st.session_state.current_token > 0:
                st.session_state.queue[st.session_state.current_token - 1]["Status"] = "Completed ✅"
            
            st.session_state.current_token += 1
            curr = st.session_state.queue[st.session_state.current_token - 1]
            curr["Status"] = "In Cabin 🩺"
            st.toast(f"Token {curr['Token']} ({curr['Name']}) ko bulaya gaya hai!")
            
            if st.session_state.current_token < len(st.session_state.queue):
                nxt = st.session_state.queue[st.session_state.current_token]
                if "WhatsApp" in nxt["Source"]:
                    st.info(f"📲 **Auto WhatsApp Alert Sent to {nxt['Name']} ({nxt['Token']}):** Abhi Token #{st.session_state.current_token:02d} doctor ke paas hain, agla number aapka hai!")
        else:
            st.warning("Line mein koi aur patient waiting nahi hai.")

    st.divider()
    st.write("### 📋 Aaj Ki Poori Patient List")
    if st.session_state.queue:
        df = pd.DataFrame(st.session_state.queue)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write("Abhi tak koi token book nahi hua hai.")
