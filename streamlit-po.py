import streamlit as st
import streamlit.components.v1 as components
from gsheetsdb import connect
import random
import pandas

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

    # components.html(
    #     """<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
    #     <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="dark" data-type="VERTICAL" data-vanity="hasiow" data-version="v1"></div>""",
    #     height=280,
    # )
    st.caption("Tomasz Hasiów | https://tomjohn.streamlit.app/")
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
    st.caption("Materials in the app used with permission of Stefan Wolpers")
    st.markdown(
        f"""
        <div class="bpad" id="bpad">
        <a href="https://www.buymeacoffee.com/tomjohn" style="color: grey; text-decoration:none;">
        <div style="justify-content: center;margin:0px; border:solid 2px;background-color: #0e1117; ;border-radius:10px; border-color:#21212f; width: fit-content;padding:0.425rem">
        <img src="https://raw.githubusercontent.com/TomJohnH/streamlit-game/main/images/coffe.png" style="max-width:20px;margin-right:10px;">
        Buy me a coffee</a></div></div>""",
        unsafe_allow_html=True,
    )

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

tab1, tab2 = st.tabs(["Flashcards", "Search engine"])


# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
# As seen here: https://docs.streamlit.io/knowledge-base/tutorials/databases/public-gsheet


# @st.cache_data(ttl=600)
@st.cache_resource
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


with tab1:
    # st.title("Product Owner Interview Questions Flashcards")
    no = len(rows)
    st.caption("Currently we have " + str(no) + " questions in the database")

    # ---------------- Questions & answers logic ----------------

    col1, col2 = st.columns(2)
    with col1:
        question = st.button(
            "Draw question", on_click=callback, key="Draw", use_container_width=True
        )
    with col2:
        answer = st.button(
            "Show answer", on_click=callback2, key="Answer", use_container_width=True
        )

    if question or st.session_state.button_clicked:
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

        if answer:
            st.markdown(
                f"<div class='answer'><span style='font-weight: bold; color:#6d7284;'>Answer to question number {st.session_state.q_no_temp+1}</span><br><br>{rows[st.session_state.q_no_temp].Answer}</div>",
                unsafe_allow_html=True,
            )
            st.session_state.button2_clicked = False

    # this part normally should be on top however st.markdown always adds divs even it is rendering non visible parts?

    st.markdown(
        '<div><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Barlow+Condensed&family=Cabin&display=swap" rel="stylesheet"></div>',
        unsafe_allow_html=True,
    )

with tab2:

    # great use case: https://discuss.streamlit.io/t/create-a-search-engine-with-streamlit-and-google-sheets/39349

    # convert data to pandas dataframe

    df = pandas.DataFrame(rows)

    # Use a text_input to get the keywords to filter the dataframe
    text_search = st.text_input("Search in titles, questions and answers", value="")

    # Filter the dataframe using masks
    m1 = df["Topic"].str.contains(text_search)
    m2 = df["Question"].str.contains(text_search)
    m3 = df["Answer"].str.contains(text_search)
    df_search = df[m1 | m2 | m3]

    # Another way to show the filtered results
    # Show the cards
    N_cards_per_row = 2
    if text_search:
        for n_row, row in df_search.reset_index().iterrows():
            i = n_row % N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
            # draw the card
            with cols[n_row % N_cards_per_row]:
                st.caption(f"Question {row['No']:0.0f}")
                st.caption(f"{row['Topic'].strip()}")
                st.markdown(f"**{row['Question'].strip()}**")
                st.markdown(f"{row['Answer'].strip()}")
                # with st.expander("Answer"):
                #     st.markdown(f"*{row['Answer'].strip()}*")
