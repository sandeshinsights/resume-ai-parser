from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import json
import re

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="moonshotai/Kimi-K2.5",
    task="conversational",
    max_new_tokens=8000,
    temperature=0.1,
)
chat = ChatHuggingFace(llm=llm)

def parse_cv_with_gemini(text):
    prompt = f"""You are an expert CV parser. Extract information in STRICT JSON format.

Rules:
- Return ONLY valid JSON, no markdown code blocks, no explanation
- Use null for missing fields
- Do NOT hallucinate any information
- Normalize skills to lowercase
- Keep descriptions short (max 10 words each)

JSON schema:
{{"name":null,"email":null,"phone":null,"location":null,"summary":null,"skills":[],"education":[{{"degree":"","institution":"","year":"","gpa":""}}],"experience":[{{"role":"","company":"","duration":"","description":[]}}],"projects":[{{"name":"","description":"","technologies":[]}}],"certifications":[],"languages":[]}}

CV text:
{text[:6000]}"""

    response = chat.invoke(prompt)
    raw = response.content.strip()

    # Clean markdown fences
    if "```json" in raw:
        raw = raw.split("```json", 1)[1]
    elif "```" in raw:
        raw = raw.split("```", 1)[1]
    if "```" in raw:
        raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()

    # Fix unterminated strings
    # Find the last { and truncate to last valid closing }
    last_brace = raw.rfind("}")
    if last_brace > 0:
        raw = raw[:last_brace + 1]
    
    # First brace
    first_brace = raw.find("{")
    if first_brace > 0:
        raw = raw[first_brace:]

    return json.loads(raw)