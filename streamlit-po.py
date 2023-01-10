import streamlit as st
import streamlit.components.v1 as components
from gsheetsdb import connect
import random

# -------------- app config ---------------

st.set_page_config(page_title="Product Owner Flashcards", page_icon="🚀")

# ---------------- functions ----------------

# external css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# callbacks
def callback():
    st.session_state.button_clicked = True


def callback2():
    st.session_state.button2_clicked = True


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.write("**Streamlit app created by:**")

    # linkedin badge: https://www.linkedin.com/pulse/how-create-linkedin-badge-your-website-amy-wallin/

    components.html(
        '<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script><div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="dark" data-type="VERTICAL" data-vanity="hasiow" data-version="v1"></div>',
        height=280,
    )
    st.caption("Tomasz Hasiów | e-mail: thasiow[at]onet.pl")
    st.write("**Questions and answers sourced from:**")
    st.caption(" 82 Product Owner Interview Questions to Avoid Hiring Imposters")
    st.caption("By Stefan Wolpers | Version 8.01 | 2022-01-17")
    st.caption("https://berlin-product-people.com/")
    st.caption(
        "Download link: https://age-of-product.com/42-scrum-product-owner-interview-questions/"
    )
    st.write("Copyright notice:")
    st.caption(
        "No part of this publication or its text may be made publicly available or, excepting personal use, reproduced, or distributed or translated into other languages without the prior written permission of Berlin Product People GmbH. If you would like permission to reproduce or otherwise publish any part or all of this publication or its text, including translations thereof, write to us at info@berlin-product-people.com addressed “Attention: Permissions Request.”"
    )
    st.caption("Materials in app used with permission of Stefan Wolpers")


# ---------------- CSS ----------------

local_css("style.css")

# ---------------- SESSION STATE ----------------

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

if "button2_clicked" not in st.session_state:
    st.session_state.button2_clicked = False

if "q_no" not in st.session_state:
    st.session_state.q_no = 0

if "q_no_temp" not in st.session_state:
    st.session_state.q_no_temp = 0

# ---------------- Main page ----------------

st.title("Product Owner Interview Questions Flashcards")

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
# As seen here: https://docs.streamlit.io/knowledge-base/tutorials/databases/public-gsheet
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


# secrets should be secrtes. shhh don't tell anyone
sheet_url = st.secrets["public_gsheets_url"]

# ok let's run the query
rows = run_query(
    f'SELECT * FROM "{sheet_url}"'
)  # f string read more here if you want https://en.wikipedia.org/wiki/Python_(programming_language)#Expressions

# how many rows were returned?
no = len(rows)
st.write("Currently we have " + str(no) + " questions in the database")

# ---------------- Questions & answers logic ----------------

if (
    st.button("Draw question", on_click=callback, key="Draw")
    or st.session_state.button_clicked
):
    # randomly select question number
    st.session_state.q_no = random.randint(0, no - 1)

    # this 'if' checks if algorithm should use value from temp or new value (temp assigment in else)
    if st.session_state.button2_clicked:
        st.markdown(
            f'<div class="blockquote-wrapper"><div class="blockquote"><h1><span style="color:#ffffff">{rows[st.session_state.q_no_temp].Question}</span></h1><h4>&mdash; Question no. {st.session_state.q_no_temp+1}</em></h4></div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="blockquote-wrapper"><div class="blockquote"><h1><span style="color:#ffffff">{rows[st.session_state.q_no].Question}</span></h1><h4>&mdash; Question no. {st.session_state.q_no+1}</em></h4></div></div>',
            unsafe_allow_html=True,
        )
        # keep memory of question number in order to show answer
        st.session_state.q_no_temp = st.session_state.q_no

    if st.button("Show answer", on_click=callback2, key="Answer"):
        st.markdown(f"Answer to question number {st.session_state.q_no_temp+1}")
        st.markdown(
            f"{rows[st.session_state.q_no_temp].Answer}", unsafe_allow_html=True
        )
        st.session_state.button2_clicked = False

# this part normally should be on top however st.markdown always adds divs even it is rendering non visible parts?

st.markdown(
    '<div><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Barlow+Condensed&family=Cabin&display=swap" rel="stylesheet"></div>',
    unsafe_allow_html=True,
)
