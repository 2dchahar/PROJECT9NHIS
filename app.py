import streamlit as st
from auth import authenticate
from langchain_config import get_summary
from database import save_query, load_history
from pdf_export import export_pdf
from dashboard import sector_dashboard
from agents import investment_agent

st.set_page_config(page_title="Equity Research Tool", layout="wide")

# Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(u, p):
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")
    st.stop()

st.title("📈 Equity Research News Tool")

query = st.text_input("Enter market or company query")

if st.button("Analyze"):
    summary = get_summary(query)
    sentiment = investment_agent(summary)
    save_query(query, summary)

    st.subheader("Summary")
    st.write(summary)

    st.subheader("AI Agent Recommendation")
    st.success(sentiment)

    if st.button("Export PDF"):
        path = export_pdf(query, summary)
        st.download_button("Download PDF", open(path, "rb"))

st.subheader("Sector Dashboard")
st.plotly_chart(sector_dashboard())

st.subheader("Query History")
for q, s in load_history():
    st.markdown(f"**{q}** — {s[:120]}...")
