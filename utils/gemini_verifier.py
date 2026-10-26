import os
import json

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing from .env"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# DEFAULT RESULT
# ============================================================

def default_result(message):

    return {
        "job_page_found": False,
        "url_accessible": False,

        "extracted_company": "",
        "extracted_job_title": "",
        "extracted_location": "",
        "extracted_salary": "",
        "job_id": "",

        "official_company_domain": "",
        "official_job_url": "",

        "job_existence": "not_confirmed",
        "official_match": "unknown",

        "risk_score": 50,
        "risk_level": "medium",
        "confidence": 0,

        "reasons": [message],
        "suspicious_indicators": [],
        "supporting_sources": [],

        "summary": message
    }


# ============================================================
# MAIN GEMINI VERIFICATION
# ============================================================

def verify_job_with_gemini(
    job_url,
    company_name="",
    job_title="",
    location="",
    salary="",
    recruiter_name="",
    description=""
):

    print()
    print("========================================")
    print("STARTING GEMINI JOB VERIFICATION")
    print("========================================")
    print("URL:", job_url)
    print()


    # --------------------------------------------------------
    # URL CHECK
    # --------------------------------------------------------

    if not job_url:

        return default_result(
            "No job URL was provided."
        )


    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are the AI verification engine for JobShield,
a fake job detection and verification system.

Your task is to analyze a submitted job advertisement
using BOTH:

1. The submitted URL using URL Context.
2. Public web information using Google Search.

You must carefully compare the submitted job with
publicly available evidence.

============================================================
SUBMITTED JOB
============================================================

JOB URL:
{job_url}

COMPANY PROVIDED BY USER:
{company_name}

JOB TITLE PROVIDED BY USER:
{job_title}

LOCATION PROVIDED BY USER:
{location}

SALARY PROVIDED BY USER:
{salary}

RECRUITER:
{recruiter_name}

DESCRIPTION:
{description}


============================================================
ANALYSIS TASKS
============================================================

1. Open and analyze the submitted job URL.

2. Determine whether the URL actually contains a job
   advertisement or relevant recruitment information.

3. Extract:
   - company name
   - job title
   - location
   - salary
   - job ID
   - company website/domain

4. Search the public web for:
   - the company
   - the company careers website
   - the submitted job title
   - the job ID if available
   - matching job listings

5. Give particular importance to the company's official
   careers/recruitment website.

6. If the same job appears on the official company website,
   compare:
   - company
   - job title
   - location
   - job ID
   - description
   - salary if available

7. Determine whether public evidence supports the existence
   of the submitted job.

8. Identify suspicious indicators such as:
   - mismatch with official company information
   - suspicious domain
   - different company name
   - inconsistent job title
   - inconsistent location
   - fake recruiter information
   - suspicious contact information
   - unrealistic salary
   - job not found where expected
   - conflicting information

9. IMPORTANT:

A job must NOT automatically be considered fake merely
because it cannot be found online.

If there is insufficient evidence, use:

"not_confirmed"

If reliable public evidence supports the job, use:

"supported"

If reliable evidence contradicts the submitted job, use:

"conflicting"

10. Never invent sources, URLs, companies, job IDs,
or evidence.

11. Return ONLY valid JSON.


============================================================
REQUIRED JSON FORMAT
============================================================

{{
    "job_page_found": false,
    "url_accessible": false,

    "extracted_company": "",
    "extracted_job_title": "",
    "extracted_location": "",
    "extracted_salary": "",
    "job_id": "",

    "official_company_domain": "",
    "official_job_url": "",

    "job_existence": "not_confirmed",
    "official_match": "unknown",

    "risk_score": 0,
    "risk_level": "low",
    "confidence": 0,

    "reasons": [],

    "suspicious_indicators": [],

    "supporting_sources": [],

    "summary": ""
}}


============================================================
ALLOWED VALUES
============================================================

job_existence:

"supported"
"not_confirmed"
"conflicting"


official_match:

"yes"
"no"
"unknown"


risk_level:

"low"
"medium"
"high"


risk_score:

Integer from 0 to 100.


confidence:

Integer from 0 to 100.


============================================================
RISK SCORE GUIDELINES
============================================================

0-29:
Low risk

30-59:
Medium risk

60-100:
High risk


============================================================
SOURCE REQUIREMENT
============================================================

supporting_sources must contain publicly accessible
URLs that were actually used as evidence.

Prioritize:

1. Official company careers website
2. Official company website
3. Established job portals
4. Other reputable public sources

Do not invent URLs.

============================================================
FINAL SUMMARY
============================================================

Provide a short explanation of why the job was classified
as supported, not_confirmed, or conflicting.
"""


    # ========================================================
    # CALL GEMINI INTERACTIONS API
    # ========================================================

    try:

        print("Calling Gemini Interactions API...")
        print()


        interaction = client.interactions.create(

            model="gemini-3.6-flash",

            input=prompt,

            tools=[
                {
                    "type": "url_context"
                },
                {
                    "type": "google_search"
                }
            ]
        )


        print("Gemini API request completed.")
        print()


        # ====================================================
        # GET RESPONSE TEXT
        # ====================================================

        response_text = interaction.output_text


        print("RAW GEMINI RESPONSE:")
        print("----------------------------------------")
        print(response_text)
        print("----------------------------------------")
        print()


        if not response_text:

            raise ValueError(
                "Gemini returned an empty response."
            )


        # ====================================================
        # CLEAN RESPONSE
        # ====================================================

        response_text = response_text.strip()


        if response_text.startswith("```json"):

            response_text = response_text[
                len("```json"):
            ]


        elif response_text.startswith("```"):

            response_text = response_text[
                len("```"):
            ]


        if response_text.endswith("```"):

            response_text = response_text[
                :-len("```")
            ]


        response_text = response_text.strip()


        # ====================================================
        # PARSE JSON
        # ====================================================

        result = json.loads(
            response_text
        )


        # ====================================================
        # DEFAULT VALUES
        # ====================================================

        result.setdefault(
            "job_page_found",
            False
        )

        result.setdefault(
            "url_accessible",
            False
        )

        result.setdefault(
            "extracted_company",
            ""
        )

        result.setdefault(
            "extracted_job_title",
            ""
        )

        result.setdefault(
            "extracted_location",
            ""
        )

        result.setdefault(
            "extracted_salary",
            ""
        )

        result.setdefault(
            "job_id",
            ""
        )

        result.setdefault(
            "official_company_domain",
            ""
        )

        result.setdefault(
            "official_job_url",
            ""
        )

        result.setdefault(
            "job_existence",
            "not_confirmed"
        )

        result.setdefault(
            "official_match",
            "unknown"
        )

        result.setdefault(
            "risk_score",
            50
        )

        result.setdefault(
            "risk_level",
            "medium"
        )

        result.setdefault(
            "confidence",
            0
        )

        result.setdefault(
            "reasons",
            []
        )

        result.setdefault(
            "suspicious_indicators",
            []
        )

        result.setdefault(
            "supporting_sources",
            []
        )

        result.setdefault(
            "summary",
            ""
        )


        # ====================================================
        # PRINT RESULT
        # ====================================================

        print("========================================")
        print("GEMINI VERIFICATION SUCCESS")
        print("========================================")

        print(
            "Job Page:",
            result["job_page_found"]
        )

        print(
            "URL Accessible:",
            result["url_accessible"]
        )

        print(
            "Company:",
            result["extracted_company"]
        )

        print(
            "Job:",
            result["extracted_job_title"]
        )

        print(
            "Job Existence:",
            result["job_existence"]
        )

        print(
            "Official Match:",
            result["official_match"]
        )

        print(
            "Risk:",
            result["risk_score"]
        )

        print(
            "Risk Level:",
            result["risk_level"]
        )

        print(
            "Confidence:",
            result["confidence"]
        )

        print("========================================")


        return result


    # ========================================================
    # JSON ERROR
    # ========================================================

    except json.JSONDecodeError as e:

        print()
        print("========================================")
        print("JSON PARSING ERROR")
        print("========================================")

        print(
            "ERROR:",
            str(e)
        )

        print("========================================")


        return default_result(
            "Gemini returned an invalid JSON response."
        )


    # ========================================================
    # API ERROR
    # ========================================================

    except Exception as e:

        print()
        print("========================================")
        print("GEMINI API ERROR")
        print("========================================")

        print(
            "ERROR TYPE:",
            type(e).__name__
        )

        print(
            "ERROR:",
            str(e)
        )

        print("========================================")


        return default_result(
            "Gemini verification was unavailable."
        )