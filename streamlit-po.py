import streamlit as st
from gsheetsdb import connect
import random
import streamlit.components.v1 as components


with st.sidebar:
    st.write("**Questions sourced from:**")
    st.write(" 82 Product Owner Interview Questions to Avoid Hiring Imposters")
    st.write("By Stefan Wolpers | Version 8.01 | 2022-01-17")
    st.write("https://berlin-product-people.com/")
    st.write("**Streamlit app created by:**")
    components.html(
        '<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script><div class="badge-base LI-profile-badge" data-locale="pl_PL" data-size="medium" data-theme="dark" data-type="VERTICAL" data-vanity="hasiow" data-version="v1"></div>',
        height=310,
    )


st.title("Product Owner Interview Questions Flashcards")


# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


# secrets should be secrtes. shhh don't tell anyone
sheet_url = st.secrets["public_gsheets_url"]

# ok let's run query
rows = run_query(
    f'SELECT * FROM "{sheet_url}"'
)  # f string read more here if you want https://en.wikipedia.org/wiki/Python_(programming_language)#Expressions

# how many rows were returned?
no = len(rows)
st.write("Currntly we have " + str(no) + " questions in the database")

# Drawing random question

if st.button("Draw question"):
    no = random.randint(0, no - 1)
    st.write(rows[no])
