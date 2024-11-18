
import streamlit as st
import yagmail
from datasets import load_dataset, Dataset, concatenate_datasets
import pandas as pd
import os

os.environ['HF_TOKEN'] = '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'


# Send Email
def send_email(hr_email, subject, body, resume_path, sender_email, sender_password):
    yag = yagmail.SMTP(user=sender_email, password=sender_password)
    yag.send(to=hr_email, subject=subject, contents=body, attachments=resume_path)

# Load existing dataset or create a new one
def load_hf_dataset(repo_id):
    try:
        dataset = load_dataset(repo_id, split="train")
        return dataset
    except Exception:
        return None

# Save data to Hugging Face dataset
def save_to_hf_dataset(repo_id, new_data, existing_dataset=None):
    try:
        # Convert new data into a Dataset
        new_dataset = Dataset.from_dict(new_data)

        # If existing dataset, concatenate with the new one
        if existing_dataset:
            updated_dataset = concatenate_datasets([existing_dataset, new_dataset])
        else:
            updated_dataset = new_dataset

        # Get Hugging Face token from environment variable
        hf_token = os.getenv('HF_TOKEN')
        if not hf_token:
            raise ValueError("Hugging Face token is missing or invalid")

        # Push the dataset to Hugging Face Hub with token authentication
        updated_dataset.push_to_hub(repo_id)
        return True
    except Exception as e:
        st.error(f"Error saving to dataset: {e}")
        return False

# Streamlit Frontend
def main():
    st.title("Email Sender")
    
    # Input fields
    hr_email = st.text_input("Enter HR's Email", placeholder="hr@example.com")
    job_profile = st.text_input("Enter Job Profile", placeholder="e.g., Python Developer")
    company_name = st.text_input("Enter Company Name", placeholder="e.g., Accenture")
    city=st.text_input("Enter City", placeholder="e.g. Pune")
    access_id=st.text_input("Enter Access ID")
    
    # Dataset repo ID
    hf_repo_id = "suzall/mails"

    # Submit button
    if st.button("Send Email"):
        if not hr_email:
            st.error("HR email is required!")
            return
        if not job_profile:
            st.error("Job profile is required!")
            return
        if not company_name:
            st.error("Company name is required!")
            return
        if not city:
            st.error("City is required!")
            return
        if not access_id:
            st.error("Access ID is required!")
            return
        
        # Backend data
        resume_path = "SujalTamrakar.py.pdf"
       
        # Generate email
        email_body = f"""
Dear Hiring Manager,

I'm excited to apply for the {job_profile} role at {company_name}. With a strong IT background (B.Tech, CGPA: 7.97) and experience in AI, Machine Learning, and Web Development, I'm confident in my ability to contribute to your team.

Key Highlights:

- AI Intern at VKAPS IT Solutions: Built & deployed AI projects using LangChain Python OpenAI
- Data Science Trainee at Grow Tech: Utilized exploratory data analysis and SQL
- Projects: Online Code Review Tool, Automatic Ticket Classification Tool (details on attached resume)

Tech Skills:

- Programming: Python, SQL
- AI/ML: LangChain, LLMs, Pinecone, Cohere
- Web Dev: Streamlit
Attached: Resume (including full project details, education, and additional experience)

Contact:

- Email: sujal.tamrakar@outlook.com
- Phone: +91-7067599678
- LinkedIn: linkedin.com/in/sujaltamrakar
- GitHub: github.com/sujal03

Best Regards, Sujal Tamrakar
        """
        
        # Email configuration
        sender_email = "sanskarsujaltamrakar2903@gmail.com"
        if access_id=='2003':
            sender_password = "livb cebd xetz sgoh"
        
        # Send email
        try:
            send_email(hr_email, f"Application for {job_profile} at {company_name}", email_body, resume_path, sender_email, sender_password)
            st.success("Email sent successfully!")

            # Prepare data to store
            new_data = {
                "hr_email": [hr_email],
                "job_profile": [job_profile],
                "company_name": [company_name],
                "company_city": [city]
            }

            # Load existing dataset
            existing_dataset = load_hf_dataset(hf_repo_id)
            
            # Save data to Hugging Face dataset
            if save_to_hf_dataset(hf_repo_id, new_data, existing_dataset):
                st.success("Data saved to Hugging Face dataset successfully!")

        except Exception as e:
            st.error(f"Error sending email or saving data: {e}")

if __name__== "__main__":
    main()
