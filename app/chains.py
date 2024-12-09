import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self) -> None:
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("groq_api"), model="llama3-70b-8192")
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template( """
                                                      ### SCRAPED TEXT FROM WEBSITE:
                                                      {page_data}
                                                      ### INSTRUCTION:
                                                      The scraped text is from the career's page of a website.
                                                      Your job is to extract the job postings and get relevant content which include 
                                                      the following: `role`, `experience`, `skills`, `description`, and `company information`.
                                                      Please make sure that the response should be in valid JSON format and should not contain any preamble.
                                                      ### VALID JSON RESPONSE:
                                                      """)
        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={'page_data': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            job_info = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Not able to parse job")
        return job_info if isinstance(job_info, list) else [job_info]
    def write_mail(self, job_info, resume_text):
        prompt_template = PromptTemplate.from_template("""
                                                       ### RESUME:
                                                       {resume_text}
                                                       ### JOB POSTING:
                                                       {job_posting}
                                                       ### INSTRUCTION:
                                                       You are job applicant, Based on the resume and job posting which is a JSON object with following keys: `role`, `experience`, `skills` and `description`.
                                                       , generate a cold email (add subject and follow proper format of a E-Mail) for the job application highlighting your experiences (calculate form the resume), 
                                                       skills and how can you contribute to the team. How your values and skills align with the company goals. 
                                                       Make sure to describe any relevant projects which should align with the skills in the job posting
                                                       Also make sure to add links (at the bottom after regards) of the portfolio, github, mailID, phone number or other relevant links required in proper format.
                                                       please make sure not to exceed 450 words limit. do not provide a preamble.
                                                       ### RESPONSE (NO PREAMBLE):
                                                       """)
        chain = prompt_template | self.llm
        response = chain.invoke(input={"resume_text": resume_text, "job_posting": job_info})
        print(response.content)