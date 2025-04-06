import requests
import re
import streamlit as st
def analyze_query_with_mistral(query):
    # Assuming MISTRAL_API_KEY is in env vars or a .env file
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

    system_prompt = """
You are an assistant that extracts job-related attributes from user queries to choose which script to run.
Return a JSON with the following fields:
- keywords (list of strings)
- job_family (string or null)
- job_level (string or null)
- industry (string or null)
- language (string or null)
- job_category (string or null)
"""

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"},
        json={
            "model": "open-mistral-7b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "max_tokens": 300,
            "temperature": 0.3,
        },
    )

    result = response.json()["choices"][0]["message"]["content"]

    try:
        import json
        return json.loads(result)
    except Exception:
        return {
            "keywords": re.findall(r"\b\w+\b", query),
            "job_family": None,
            "job_level": None,
            "industry": None,
            "language": None,
            "job_category": None
        }
