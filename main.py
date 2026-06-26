import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_autorefresh import st_autorefresh
import time

st.write("Time:", time.time())
st_autorefresh(interval=1000, key="refresh")
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

from google.oauth2 import service_account
from google.auth.transport.requests import Request

creds = service_account.Credentials.from_service_account_file(
    "serviceAccountKey.json"
)

try:
    creds.refresh(Request())
    st.success("TOKEN OK")
except Exception as e:
    st.error(e)

db = firestore.client()

homework_db = db.collection("main").document("homework")
activities_db = db.collection("main").document("activities")
announcements_db = db.collection("main").document("announcements")
class_tests_db = db.collection("main").document("class_tests")

st.set_page_config(layout="wide")

st.markdown("""
<style>
div.stButton > button {
    height: 40px !important;
    width: 140px !important;
    font-size: 30px !important;
    border-radius: 12px !important;
    background-color: #191970 !important;
    color: white !important;
}

div.stButton > button * {
    font-family: "Courier New", monospace !important;
    font-weight: bold !important;
}

h1, h2 {
    font-family: "Georgia", serif !important;
    font-weight: bold !important;
}

h3 {
    font-family: "Courier New", monospace !important;
    font-size: 23px !important;
}

[data-testid="column"]:nth-of-type(1){
    background-color:#F0F2F6;
    border-radius:10px;
    padding:20px;
}

div[data-baseweb="input"] input {
    font-family: 'Courier New', monospace !important;
    font-size: 24px !important;
    color: white !important;
}

div[data-testid="stWidgetLabel"] p {
    font-family: 'Courier New', monospace !important;
    font-size: 18px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([10, 1, 1])
col4, col5, col6 = st.columns([10, 1, 1])
col7, col8, col9 = st.columns([10, 1, 1])
col10, col11, col12 = st.columns([10, 1, 1])
col13, col14, col15 = st.columns([10, 1, 1])

with col1:
    st.title("Student Assignment Tracker [v1.0]")

with col4:
    for _ in range(10):
        st.text("")

    st.markdown("""
    <div style="
        background-color:#a69b03;
        padding:20px;
        border-radius:10px;
    ">
        <h3>ANNOUNCEMENTS</h3>
    </div>
    """, unsafe_allow_html=True)

    doc = announcements_db.get()

    if doc.exists:
        announcements_dict = doc.to_dict()

        for key, value in announcements_dict.items():
            st.code(f"{value}", language="html")
        if not announcements_dict:
            st.code(f"None", language="html")

with col7:
    for _ in range(5):
        st.text("")

    st.markdown("""
    <div style="
        background-color:#a34903;
        padding:20px;
        border-radius:10px;
    ">
        <h3>HOMEWORK ASSIGNMENTS</h3>
    </div>
    """, unsafe_allow_html=True)

    doc = homework_db.get()

    if doc.exists:
        homework_dict = doc.to_dict()

        for key, value in homework_dict.items():
            st.code(f"{key} : {value}", language="html")
        if not homework_dict:
            st.code(f"None", language="html")

with col10:
    for _ in range(5):
        st.text("")

    st.markdown("""
    <div style="
        background-color:#166bf5;
        padding:20px;
        border-radius:10px;
    ">
        <h3>ACTIVITIES</h3>
    </div>
    """, unsafe_allow_html=True)

    doc = activities_db.get()

    if doc.exists:
        activities_dict = doc.to_dict()

        for key, value in activities_dict.items():
            st.code(f"{key} : {value}", language="html")
        if not activities_dict:
            st.code(f"None", language="html")

with col13:
    for _ in range(5):
        st.text("")

    st.markdown("""
    <div style="
        background-color:#03a619;
        padding:20px;
        border-radius:10px;
    ">
        <h3>CLASS TESTS</h3>
    </div>
    """, unsafe_allow_html=True)

    doc = class_tests_db.get()

    if doc.exists:
        class_tests_dict = doc.to_dict()

        for key, value in class_tests_dict.items():
            st.code(f"{key} : {value}", language="html")

        if not class_tests_dict:
            st.code(f"None", language="html")

for _ in range(10):
    st.text("")

st.subheader("©️ Student Assignment Tracker (K.L.E Society's School, Rajajinagar) - Designed & Created by Aaditya Awati 2026")
