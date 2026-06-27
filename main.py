import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json

from google.oauth2 import service_account
from google.cloud import firestore

st_autorefresh(interval=1000, key="refresh")

@st.cache_resource
def get_db():
    key_dict = json.loads(st.secrets["firebase"]["json_key"])
    creds = service_account.Credentials.from_service_account_info(
        key_dict,
        scopes=["https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/datastore"]
    )
    return firestore.Client(
        project=key_dict["project_id"],
        credentials=creds
    )

db = get_db()

homework_db      = db.collection("main").document("homework")
activities_db    = db.collection("main").document("activities")
announcements_db = db.collection("main").document("announcements")
class_tests_db   = db.collection("main").document("class_tests")

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

col1,  col2,  col3  = st.columns([10, 1, 1])
col4,  col5,  col6  = st.columns([10, 1, 1])
col7,  col8,  col9  = st.columns([10, 1, 1])
col10, col11, col12 = st.columns([10, 1, 1])
col13, col14, col15 = st.columns([10, 1, 1])

with col1:
    st.title("Student Assignment Tracker [v1.0]")

with col4:
    for _ in range(10):
        st.text("")
    st.markdown("""
    <div style="background-color:#a69b03;padding:20px;border-radius:10px;">
        <h3>ANNOUNCEMENTS</h3>
    </div>""", unsafe_allow_html=True)

    doc = announcements_db.get()
    if doc.exists:
        d = doc.to_dict()
        for key, value in d.items():
            st.code(f"{value}", language="html")
        if not d:
            st.code("None", language="html")

with col7:
    for _ in range(5):
        st.text("")
    st.markdown("""
    <div style="background-color:#a34903;padding:20px;border-radius:10px;">
        <h3>HOMEWORK ASSIGNMENTS</h3>
    </div>""", unsafe_allow_html=True)

    doc = homework_db.get()
    if doc.exists:
        d = doc.to_dict()
        for key, value in d.items():
            st.code(f"{key} : {value}", language="html")
        if not d:
            st.code("None", language="html")

with col10:
    for _ in range(5):
        st.text("")
    st.markdown("""
    <div style="background-color:#166bf5;padding:20px;border-radius:10px;">
        <h3>ACTIVITIES</h3>
    </div>""", unsafe_allow_html=True)

    doc = activities_db.get()
    if doc.exists:
        d = doc.to_dict()
        for key, value in d.items():
            st.code(f"{key} : {value}", language="html")
        if not d:
            st.code("None", language="html")

with col13:
    for _ in range(5):
        st.text("")
    st.markdown("""
    <div style="background-color:#03a619;padding:20px;border-radius:10px;">
        <h3>CLASS TESTS</h3>
    </div>""", unsafe_allow_html=True)

    doc = class_tests_db.get()
    if doc.exists:
        d = doc.to_dict()
        for key, value in d.items():
            st.code(f"{key} : {value}", language="html")
        if not d:
            st.code("None", language="html")

for _ in range(10):
    st.text("")

st.subheader("©️ Student Assignment Tracker (K.L.E Society's School, Rajajinagar) - Designed & Created by Aaditya Awati 2026")
