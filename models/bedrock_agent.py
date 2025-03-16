import boto3
import json
import os

class BedrockAgentManager:
    def __init__(self, region_name=None, profile_name=None):
        """
        Initialize the Bedrock Agent Manager.
        
        Args:
            region_name (str, optional): AWS region name
            profile_name (str, optional): AWS profile name
        """
        self.region_name = region_name or os.environ.get("AWS_REGION", "eu-west-1")
        self.profile_name = profile_name or os.environ.get("AWS_PROFILE", "default")
        
        session = boto3.Session(region_name=self.region_name, profile_name=self.profile_name)
        self.bedrock_client = session.client('bedrock-runtime')
        
        # Model IDs - using Amazon's Nova models
        self.primary_model_id = "us.amazon.nova-micro-v1:0"  # For detailed analysis

    def invoke_model(self, prompt, model_id, max_tokens=4000, temperature=0.7):
        """
        Invoke a model using the Bedrock runtime API.
        
        Args:
            prompt (str): The prompt text
            model_id (str): Bedrock model ID
            max_tokens (int): Maximum tokens to generate
            temperature (float): Temperature for generation
            
        Returns:
            str: Model response
        """
        # Define one or more messages using the "user" and "assistant" roles.
        message_list = [{"role": "user", "content": [{"text": prompt}]}]
        try:
            if "amazon.nova" in model_id:
                request_body = {
                    "messages": message_list,
                    "inferenceConfig": {
                        "maxTokens": max_tokens,
                        "temperature": temperature,
                        "topP": 0.9
                    }
                }
            else:
                # Default format for other models
                request_body = {
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            
            # Invoke model
            response = self.bedrock_client.converse(
                modelId=model_id,
                messages=message_list,
                inferenceConfig={
                    "maxTokens": max_tokens,
                    "temperature": temperature,
                    "topP": 0.9
                }
            )
        
                
        except Exception as e:
            print(f"Error invoking model: {str(e)}")
            raise

        # Parse the response from the Converse API
        return response["output"]["message"]["content"][0]["text"]

    
    def analyze_cv(self, cv_text):
        """
        Analyze the CV text and extract key information.
        
        Args:
            cv_text (str): The CV text content
            
        Returns:
            dict: Extracted information from the CV
        """
        prompt = f"""
        Analyze the following CV/resume and extract key information:
        
        {cv_text}
        
        Please extract and organize the following information:
        1. Name
        2. Contact information
        3. Skills (technical and soft skills)
        4. Work experience (company names, positions, dates, and key responsibilities)
        5. Education (degrees, institutions, dates)
        6. Certifications
        7. Projects (if any)
        
        Format the output as a structured JSON.
        """
        
        response_text = self.invoke_model(prompt=prompt, model_id=self.primary_model_id  , max_tokens=2000)
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                # If no JSON found, return the text as a dict
                return {"raw_analysis": response_text}
        except:
            return {"raw_analysis": response_text}
    
    def analyze_job_description(self, job_description):
        """
        Analyze the job description and extract key requirements.
        
        Args:
            job_description (str): The job description text
            
        Returns:
            dict: Extracted requirements from the job description
        """
        prompt = f"""
        Analyze the following job description and extract key information:
        
        {job_description}
        
        Please extract and organize the following information:
        1. Job title
        2. Company name (if available)
        3. Required skills
        4. Required experience
        5. Required education
        6. Responsibilities
        7. Nice-to-have qualifications
        
        Format the output as a structured JSON.
        """
        
        response_text = self.invoke_model(prompt=prompt, model_id=self.primary_model_id, max_tokens=2000)
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                # If no JSON found, return the text as a dict
                return {"raw_analysis": response_text}
        except:
            return {"raw_analysis": response_text}
    
    def generate_cv_improvement_suggestions(self, cv_analysis, job_analysis):
        """
        Generate suggestions to improve the CV based on the job description.
        
        Args:
            cv_analysis (dict): Analysis of the CV
            job_analysis (dict): Analysis of the job description
            
        Returns:
            dict: Suggestions for CV improvement
        """
        prompt = f"""
        I need you to act as a career coach and provide suggestions to improve a CV/resume to better match a specific job description.
        
        Here is the analysis of the CV:
        {json.dumps(cv_analysis, indent=2)}
        
        Here is the analysis of the job description:
        {json.dumps(job_analysis, indent=2)}
        
        Please provide detailed suggestions on how to improve the CV to better match this job description. Include:
        
        1. Skills gap analysis: What skills mentioned in the job description are missing from the CV?
        2. Experience alignment: How can the work experience be better presented to match the job requirements?
        3. Specific wording suggestions: What keywords from the job description should be incorporated?
        4. Sections to add or emphasize: What parts of the CV need more attention?
        5. General formatting or structure improvements
        
        Format your response as a structured JSON with these categories.
        """
        
        response_text = self.invoke_model(prompt=prompt, model_id=self.primary_model_id, max_tokens=4000)
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                # If no JSON found, return the text as a dict
                return {"suggestions": response_text}
        except:
            return {"suggestions": response_text}
