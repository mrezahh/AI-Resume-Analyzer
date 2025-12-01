
import json
import ollama

MODEL_NAME = "llama3.2:1b"


def analyze_resume_with_ai(resume_text: str) -> dict:
    """    Sends resume text to the local Ollama model and returns response."""
    prompt = f"""
    Analyze the following resume and extract the following information in JSON format:
    - Name
    - Email
    - Phone Number
    - Skills (as a list)
    - Experience Summary

    Resume Text:
    {resume_text}

    Provide the output in the following JSON format:
    {{
        "Name": "",
        "Email": "",
        "Phone Number": "",
        "Skills": [],
        "Experience Summary": ""
    }}
    """

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured information from resumes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.2
        )

        # Extract AI text output
        ai_output = response['message']['content']
        # Remove code block formatting if present
        if ai_output.startswith("```") and ai_output.endswith("```"):
            ai_output = ai_output.strip("```").strip()
        # convert to dict
        result = json.loads(ai_output)
        return result

    except Exception as e:
        print(f"Error analyzing resume with AI: {e}")
        return {
            'name': None,
            'email': None,
            'phone_number': None,
            'skills': [],
            'experience_summary': None,
        }