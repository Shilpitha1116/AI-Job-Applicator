import streamlit as st
import requests

def main():
    st.set_page_config(page_title="Dice Automation Tool", page_icon=":briefcase:", layout="centered")

    # Header Section
    st.title("Job Search Automation Tool")
    st.markdown("Automate your job applications effortlessly.")

    # Input Fields
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    location = st.text_input("Location", placeholder="Enter job location")
    resume_file = st.file_uploader("Upload Resume (PDF only)", type="pdf")
    threshold = st.slider("Threshold", min_value=0.0, max_value=1.0, value=0.8, step=0.01)

    # Button to trigger API
    if st.button("Submit"):
        # Validate inputs
        if not email or not password or not resume_file:
            st.error("Please fill all fields and upload your resume.")
        else:
            # Prepare form-data
            files = {
                "email": (None, email),
                "password": (None, password),
                "location": (None, location),
                "resume": (resume_file.name, resume_file.getvalue(), "application/pdf"),
                "threshold": (None, str(threshold))
            }

            # Send POST request to Flask API
            with st.spinner("Processing..."):
                try:
                    response = requests.post("http://127.0.0.1:5000/automate-dice", files=files)

                    # Handle response
                    if response.status_code == 200:
                        st.success("Response:")
                        st.json(response.json())
                    else:
                        st.error(f"Error: {response.status_code}")
                        st.json(response.json())
                except requests.exceptions.RequestException as e:
                    st.error("Failed to connect to the API.")
                    st.text(str(e))

if __name__ == "__main__":
    main()
