import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import os
import sys

st_autorefresh(interval=30000, key="refresh")

PROJECT_ID = st.secrets["firebase"]["project_id"]
API_KEY = st.secrets["firebase"]["api_key"]

BASE_URL = (
    f"https://firestore.googleapis.com/v1/"
    f"projects/{PROJECT_ID}/databases/(default)/documents/main"
)

def get_document(doc_name: str) -> dict:
    url = f"{BASE_URL}/{doc_name}?key={API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        raw_fields = resp.json().get("fields", {})
        return {
            k: list(v.values())[0]
            for k, v in raw_fields.items()
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Could not load {doc_name}: {e}")
        return {}

notifications_lib_path = os.path.abspath("streamlit-push-notifications")
sys.path.insert(0, notifications_lib_path)

import streamlit_push_notifications

if "previous_announcements" not in st.session_state:
    st.session_state.previous_announcements = {}

if "previous_homework" not in st.session_state:
    st.session_state.previous_homework = {}

if "previous_activities" not in st.session_state:
    st.session_state.previous_activities = {}

if "previous_class_tests" not in st.session_state:
    st.session_state.previous_class_tests = {}

announcements_data = get_document("announcements")
homework_data = get_document("homework")
activities_data = get_document("activities")
class_tests_data = get_document("class_tests")

if st.session_state.previous_announcements:
    new_items = {
        k: v
        for k, v in announcements_data.items()
        if k not in st.session_state.previous_announcements
    }

    if new_items:
        streamlit_push_notifications.send_push(
            title="New Announcement",
            body=f"{len(new_items)} new announcement(s) posted.",
            icon_path="path_to_icon.png",
            sound_path="path_to_sound.mp3",
            tag="announcements"
        )

if st.session_state.previous_homework:
    new_items = {
        k: v
        for k, v in homework_data.items()
        if k not in st.session_state.previous_homework
    }

    if new_items:
        streamlit_push_notifications.send_push(
            title="New Homework Assignment",
            body=f"{len(new_items)} new homework assignment(s) uploaded.",
            icon_path="path_to_icon.png",
            sound_path="path_to_sound.mp3",
            tag="homework"
        )

if st.session_state.previous_activities:
    new_items = {
        k: v
        for k, v in activities_data.items()
        if k not in st.session_state.previous_activities
    }

    if new_items:
        streamlit_push_notifications.send_push(
            title="New Activity",
            body=f"{len(new_items)} new activity(s) added.",
            icon_path="path_to_icon.png",
            sound_path="path_to_sound.mp3",
            tag="activities"
        )

if st.session_state.previous_class_tests:
    new_items = {
        k: v
        for k, v in class_tests_data.items()
        if k not in st.session_state.previous_class_tests
    }

    if new_items:
        streamlit_push_notifications.send_push(
            title="New Class Test",
            body=f"{len(new_items)} new class test(s) scheduled.",
            icon_path="kle_logo.jpg",
            sound_path="path_to_sound.mp3",
            tag="class_tests"
        )

st.session_state.previous_announcements = announcements_data.copy()
st.session_state.previous_homework = homework_data.copy()
st.session_state.previous_activities = activities_data.copy()
st.session_state.previous_class_tests = class_tests_data.copy()
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
    <div style="background-color:#a69b03;padding:20px;border-radius:10px;">
        <h3>ANNOUNCEMENTS</h3>
    </div>""", unsafe_allow_html=True)

    d = announcements_data
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

    d = homework_data
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

    d = activities_data
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

    d = class_tests_data
    for key, value in d.items():
        st.code(f"{key} : {value}", language="html")
    if not d:
        st.code("None", language="html")

for _ in range(10):
    st.text("")

st.subheader("©️ Student Assignment Tracker (K.L.E Society's School, Rajajinagar) - Designed & Created by Aaditya Awati 2026")
