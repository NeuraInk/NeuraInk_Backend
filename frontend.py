import streamlit as st
import os
import requests

backend_url = "http://localhost:8000"

st.title('Process')

file_path = st.text_input("File Path: ")

submit = st.button('Submit')

if submit:
    body = {
        "file_path": file_path,
    }
    res = requests.post(backend_url + f"/process/", json=body)
    res = res.json
    st.write(res.success)