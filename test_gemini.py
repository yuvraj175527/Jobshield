from utils.gemini_verifier import verify_job_with_gemini


result = verify_job_with_gemini(

    job_url="https://careers.microsoft.com/",

    company_name="Microsoft",

    job_title="Software Engineer",

    location="India",

    salary="",

    recruiter_name="",

    description="Software engineering position at Microsoft."
)


print()
print("========================================")
print("GEMINI JOB VERIFICATION RESULT")
print("========================================")

print(result)

print("========================================")