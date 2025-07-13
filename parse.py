from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time


_model_cache = {}

def get_model():
    if "gemma3" not in _model_cache:
        _model_cache["gemma3"] = OllamaLLM(model="gemma3")
    return _model_cache["gemma3"]

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_ollama(dom_content, parse_description, max_retries=2):
    prompt = ChatPromptTemplate.from_template(template)
    model = get_model()
    chain = prompt | model
    
    retries = 0
    while retries <= max_retries:
        try:
            response = chain.invoke({
                "dom_content": dom_content, 
                "parse_description": parse_description
            })
            return response
        except Exception as e:
            retries += 1
            if retries > max_retries:
                raise Exception(f"Failed to parse content after {max_retries} attempts: {str(e)}")
            time.sleep(1)  # Brief pause before retrying