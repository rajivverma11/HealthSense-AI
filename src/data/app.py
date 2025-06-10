import streamlit as st
import requests

st.title("HealthSense AI Chat")

name = st.text_input("Your full name")
query = st.text_area("What would you like to know?")

if st.button("Submit"):
    if name and query:
        with st.spinner("Thinking..."):
            response = requests.post("http://localhost:8000/ask", json={"name": name, "query": query})
            result = response.json()
            st.markdown("### Response:")
            st.write(result.get("answer", result.get("error", "Something went wrong.")))
    else:
        st.warning("Please enter both name and query.")
