import streamlit as st
from init_proj import init

# import pandas as pd

st.sidebar.title("Project initialization")
st.sidebar.text("Input path to the project directory\nWe will create a directory structure\n and template config")

basedir = ""
basedir = st.sidebar.text_input("Base directory")
if basedir == "":
    st.sidebar.text("(Enter a path and press Enter\nThen press the button below)")
else:
    st.sidebar.text(basedir)

st.sidebar.text("Project name will be used as\nname suffix for dirs and files")
projname = st.sidebar.text_input("Project Name")

if st.sidebar.button("Create base dir"):
    message = init(basedir, projname)
    for line in message.split("\n"):
        st.write(line)
