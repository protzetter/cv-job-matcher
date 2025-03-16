# CV Job Matcher
![](image.png)
A Streamlit application that helps users improve their CV/resume to better match job descriptions using Amazon Bedrock's AI capabilities.

## Features

- Upload and parse CV/resume in PDF format
- Scrape job descriptions from URLs or paste them directly
- Analyze CVs and job descriptions using Amazon Bedrock's Nova models
- Generate tailored CV improvement suggestions
- Identify skills gaps and keyword opportunities
- Provide formatting and content recommendations

## Architecture

This application uses:
- **Streamlit**: For the web interface
- **Amazon Bedrock**: For AI-powered analysis and suggestions
  - Amazon Nova Micro: For detailed analysis and suggestions
- **BeautifulSoup4**: For web scraping job descriptions
- **PyPDF2**: For parsing PDF resumes

## Setup and Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd cv_job_matcher
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure AWS credentials:
   - Update a `.env` file
   - Set your AWS region and profile

4. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

## AWS Permissions Required

The application requires the following AWS permissions:
- `bedrock:InvokeModel` for Nova Micro models

## Usage

1. Upload your CV/resume (PDF format)
2. Provide a job description (URL or paste text)
3. Analyze both the CV and job description
4. Generate tailored improvement suggestions
5. Review the suggestions to improve your CV

## Project Structure

```
cv_job_matcher/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── data/                   # Data storage directory
├── models/
│   └── bedrock_agent.py    # Bedrock integration for AI analysis
├── utils/
│   ├── pdf_parser.py       # PDF parsing utilities
│   └── web_scraper.py      # Web scraping utilities
└── templates/              # HTML templates (if needed)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
