
import json
import ollama

MODEL_NAME = "llama3.2:1b"


def analyze_resume_with_ai(resume_text: str) -> dict:
    """    Sends resume text to the local Ollama model and returns response."""
    prompt = f"""
    Analyze the following resume and provide structured feedback in JSON format.

    Resume Text:
    {resume_text}

    Extract and return the following:
    - Name
    - Email
    - Phone Number
    - Skills (as a list)
    - Experience Summary
    - Skill Gaps (as a list)
    - Weak Points (as a list)
    - Matching Job Titles (as a list)
    - Suggestions to improve (as a list)

    JSON format:
    {{
        "name": "",
        "email": "",
        "phone_number": "",
        "skills": [],
        "experience_summary": "",
        "skill_gaps": [],
        "weak_points": [],
        "matching_job_titles": [],
        "suggestions": []
    }}
    """

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content":  "You are an expert career coach and resume analyzer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.2
        )

        # Extract AI text output
        ai_output = response['message']['content']
        
        # Remove code block formatting if present
        if ai_output.startswith("```") and ai_output.endswith("```"):
            ai_output = ai_output.strip("```").strip()
        
        # convert ai output to dict
        result = json.loads(ai_output)
        
        # Ensure keys exist
        keys = ["name", "email", "phone_number", "skills", "experience_summary",
                "skill_gaps", "weak_points", "matching_job_titles", "suggestions"]
        for k in keys:
            if k not in result:
                result[k] = [] if k in ["skills", "skill_gaps", "weak_points", "matching_job_titles", "suggestions"] else None
        
        return result

    except Exception as e:
        print(f"Error analyzing resume with AI: {e}")
        return {
            'name': None,
            'email': None,
            'phone_number': None,
            'skills': [],
            'experience_summary': None,
            'skill_gaps': [],
            'weak_points': [],
            'matching_job_titles': [],
            'suggestions': [],
        }

def match_resume_to_jobs(resume: Resume, jobs: list[Job]):
    resume_skills = set(resume.skills.split(','))
    matched = []
    for job in jobs:
        job_skills = set(job.required_skills.split(','))
        score = len(resume_skills & job_skills) / len(job_skills)
        if score > 0.3:  # threshold
            matched.append({"job_id": job.id, "title": job.title, "match_score": score})
    return matched
