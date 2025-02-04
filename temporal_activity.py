import requests
from bs4 import BeautifulSoup
from openai import AzureOpenAI
import json
import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = 'gpt-4o'
api_version = "2023-07-01-preview"

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    base_url=f"{api_base}/openai/deployments/{deployment_name}/models"
)

def fetch_html(url):
    """Fetch HTML content from the URL"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Successfully fetched the HTML content.")
            return response.text
        else:
            print(f"Failed to fetch the URL. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to fetch the URL: {e}")
        return None


def parse_html(content):
    """Use BeautifulSoup to extract textual content"""
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)
    return text


def extract_api_info_with_openai(parsed_text):
    prompt = f"""
    Extract the following information from the API Documentation:
    - The entities (models) and their fields.
    - The supported authentication types.
    - The available API endpoints.
    - The rate-limiting details: limits on requests per minute/hour, rate limit headers, and retry guidelines.
    - Include any specific headers or fields that pertain to rate limiting.
    Here is the API documentation:
    {parsed_text}

    Provide your response in JSON format:
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=1000,
        temperature=0.2
    )

    if response and response.choices:
        return response.choices[0].message.content
    else:
        print("No valid response returned by OpenAI API.")
        return None


# Define the Temporal activity
async def process_api_documentation(api_docs_url: str):
    html_content = fetch_html(api_docs_url)
    if html_content:
        parsed_text = parse_html(html_content)
        if parsed_text:
            return extract_api_info_with_openai(parsed_text)
        else:
            return "Error: Failed to parse HTML content."
    else:
        return "Error: Failed to fetch HTML content."
