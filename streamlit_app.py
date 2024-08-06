import streamlit as st
from streamlit_quill import st_quill
import requests

def generate_report(subreddit_name):
    response = requests.post("http://localhost:5000/generate_report", json={"subreddit_name": subreddit_name})
    if response.status_code == 200:
        return response.json().get("filtered_html_content")
    else:
        st.error("Failed to generate report.")
        return ""

def send_report(edited_report):
    response = requests.post("http://localhost:5000/send_report", json={"edited_report": edited_report})
    if response.status_code == 200:
        return response.json().get("telegraph_url")
    else:
        st.error("Failed to send report.")
        return ""

def main():
    st.set_page_config(page_title="Research Report Generator", layout="wide")
    st.title("Research Report Generator")

    with st.sidebar:
        subreddit_name = st.text_input("Enter Subreddit Name", placeholder="LocalLLaMA")

    # Initialize session state for editor content
    if 'editor_content' not in st.session_state:
        st.session_state['editor_content'] = ""

    if st.button("Generate Report", key="generate_report_button"):
        filtered_html_content = generate_report(subreddit_name)
        if filtered_html_content:
            st.session_state['editor_content'] = filtered_html_content
            st.info("Report generated and filtered. Ready for review and editing.")

    # Quill editor for editing HTML content
    edited_content = st_quill(
        value=st.session_state['editor_content'],
        html=True,
        placeholder="Edit the Research Report"
    )

    if st.button("Apply Changes", key="apply_changes_button"):
        # Update the session state with the current editor content
        st.session_state['editor_content'] = edited_content

    if st.button("Send Report", key="send_report_button"):
        telegraph_url = send_report(st.session_state['editor_content'])
        if telegraph_url:
            st.success("Report generated and sent to Telegram!")
            st.write(f"Telegraph URL: {telegraph_url}")

if __name__ == "__main__":
    main()
