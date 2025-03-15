import streamlit as st
import os
import json
from dotenv import load_dotenv
from utils.pdf_parser import extract_text_from_pdf
from utils.web_scraper import scrape_job_description
from models.bedrock_agent import BedrockAgentManager

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="CV Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'cv_text' not in st.session_state:
    st.session_state.cv_text = None
if 'job_description' not in st.session_state:
    st.session_state.job_description = None
if 'cv_analysis' not in st.session_state:
    st.session_state.cv_analysis = None
if 'job_analysis' not in st.session_state:
    st.session_state.job_analysis = None
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = None

# Initialize Bedrock Agent Manager
@st.cache_resource
def get_bedrock_agent():
    return BedrockAgentManager()

# Main app header
st.title("CV Job Matcher")
st.markdown("""
This application helps you improve your CV/resume to better match job descriptions.
Upload your CV, provide a job description URL, and get AI-powered suggestions!
""")

# Sidebar for AWS configuration
with st.sidebar:
    st.header("AWS Configuration")
    aws_region = st.text_input("AWS Region", value=os.environ.get("AWS_REGION", "us-east-1"))
    aws_profile = st.text_input("AWS Profile", value=os.environ.get("AWS_PROFILE", "default"))
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This application uses Amazon Bedrock's Nova models to:
    - Analyze your CV/resume
    - Analyze job descriptions
    - Generate tailored improvement suggestions
    
    Powered by:
    - Amazon Nova Micro
    """)

# Create tabs for the application flow
tab1, tab2, tab3 = st.tabs(["Upload CV", "Job Description", "Suggestions"])

# Tab 1: CV Upload
with tab1:
    st.header("Upload Your CV/Resume")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        try:
            with st.spinner("Extracting text from PDF..."):
                cv_text = extract_text_from_pdf(uploaded_file)
                st.session_state.cv_text = cv_text
                
                # Display a preview of the extracted text
                with st.expander("Preview Extracted Text"):
                    st.text_area("CV Content", cv_text, height=300)
                
                # Analyze the CV with Bedrock
                if st.button("Analyze CV"):
                    with st.spinner("Analyzing CV with AI..."):
                        bedrock_agent = get_bedrock_agent()
                        cv_analysis = bedrock_agent.analyze_cv(cv_text)
                        st.session_state.cv_analysis = cv_analysis
                        
                        # Display the analysis
                        st.success("CV Analysis Complete!")
                        with st.expander("View CV Analysis"):
                            st.json(cv_analysis)
        
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")

# Tab 2: Job Description
with tab2:
    st.header("Job Description")
    
    # Option to input job URL or paste job description
    input_method = st.radio("Choose input method:", ["URL", "Paste Text"])
    
    if input_method == "URL":
        job_url = st.text_input("Enter job posting URL:")
        
        if job_url and st.button("Scrape Job Description"):
            try:
                with st.spinner("Scraping job description..."):
                    job_description = scrape_job_description(job_url)
                    st.session_state.job_description = job_description
                    
                    # Display the scraped job description
                    with st.expander("Preview Job Description"):
                        st.text_area("Scraped Content", job_description, height=300)
                    
                    # Analyze the job description with Bedrock
                    if st.button("Analyze Job Description"):
                        with st.spinner("Analyzing job description with AI..."):
                            bedrock_agent = get_bedrock_agent()
                            job_analysis = bedrock_agent.analyze_job_description(job_description)
                            st.session_state.job_analysis = job_analysis
                            
                            # Display the analysis
                            st.success("Job Analysis Complete!")
                            with st.expander("View Job Analysis"):
                                st.json(job_analysis)
            
            except Exception as e:
                st.error(f"Error scraping job description: {str(e)}")
    
    else:  # Paste Text
        job_description = st.text_area("Paste job description here:", height=300)
        
        if job_description and st.button("Process Job Description"):
            st.session_state.job_description = job_description
            
            # Analyze the job description with Bedrock
            with st.spinner("Analyzing job description with AI..."):
                bedrock_agent = get_bedrock_agent()
                job_analysis = bedrock_agent.analyze_job_description(job_description)
                st.session_state.job_analysis = job_analysis
                
                # Display the analysis
                st.success("Job Analysis Complete!")
                with st.expander("View Job Analysis"):
                    st.json(job_analysis)

# Tab 3: Suggestions
with tab3:
    st.header("CV Improvement Suggestions")
    
    # Check if both analyses are available
    if st.session_state.cv_analysis and st.session_state.job_analysis:
        if st.button("Generate Suggestions"):
            with st.spinner("Generating CV improvement suggestions..."):
                bedrock_agent = get_bedrock_agent()
                suggestions = bedrock_agent.generate_cv_improvement_suggestions(
                    st.session_state.cv_analysis,
                    st.session_state.job_analysis
                )
                st.session_state.suggestions = suggestions
        
        # Display suggestions if available
        if st.session_state.suggestions:
            st.success("Suggestions Generated!")
            print("Suggestions:", st.session_state.suggestions)
            
            # Display skills gap analysis
            if "skills_gap_analysis" in st.session_state.suggestions:
                st.subheader("Skills Gap Analysis")
                st.write(st.session_state.suggestions["skills_gap_analysis"])
            
            # Display experience alignment
            if "experience_alignment" in st.session_state.suggestions:
                st.subheader("Experience Alignment")
                st.write(st.session_state.suggestions["experience_alignment"])
            
            # Display wording suggestions
            if "specific_wording_suggestions" in st.session_state.suggestions:
                st.subheader("Keyword Suggestions")
                st.write(st.session_state.suggestions["specific_wording_suggestions"])
            
            # Display sections to add or emphasize
            if "sections_to_add_or_emphasize" in st.session_state.suggestions:
                st.subheader("Sections to Add or Emphasize")
                st.write(st.session_state.suggestions["sections_to_add_or_emphasize"])
            
            # Display general improvements
            if "general_formatting_improvements" in st.session_state.suggestions:
                st.subheader("General Improvements")
                st.write(st.session_state.suggestions["general_formatting_improvements"])
            
            # If the response is not structured as expected
            if "suggestions" in st.session_state.suggestions:
                st.markdown(st.session_state.suggestions["suggestions"])
    
    else:
        st.info("Please complete both CV analysis and job description analysis before generating suggestions.")

# Add a footer
st.markdown("---")
st.markdown("CV Job Matcher - Powered by Amazon Bedrock and Streamlit")
