# ============================================================
# JOBSHIELD - OFFICIAL COMPANY DOMAINS
# ============================================================

OFFICIAL_DOMAINS = {

    # Technology
    "microsoft": [
        "microsoft.com"
    ],

    "google": [
        "google.com"
    ],

    "amazon": [
        "amazon.com"
    ],

    "apple": [
        "apple.com"
    ],

    "meta": [
        "meta.com"
    ],

    "ibm": [
        "ibm.com"
    ],

    "oracle": [
        "oracle.com"
    ],

    "adobe": [
        "adobe.com"
    ],

    "intel": [
        "intel.com"
    ],

    "nvidia": [
        "nvidia.com"
    ],

    # Indian IT companies
    "tcs": [
        "tcs.com"
    ],

    "tata consultancy services": [
        "tcs.com"
    ],

    "infosys": [
        "infosys.com"
    ],

    "wipro": [
        "wipro.com"
    ],

    "hcl": [
        "hcltech.com"
    ],

    "hcl technologies": [
        "hcltech.com"
    ],

    "tech mahindra": [
        "techmahindra.com"
    ],

    "accenture": [
        "accenture.com"
    ],

    "capgemini": [
        "capgemini.com"
    ],

    "cognizant": [
        "cognizant.com"
    ],

    # Indian companies
    "reliance": [
        "ril.com"
    ],

    "reliance industries": [
        "ril.com"
    ],

    "flipkart": [
        "flipkart.com"
    ],

    "swiggy": [
        "swiggy.com"
    ],

    "zomato": [
        "zomato.com"
    ],

    "paytm": [
        "paytm.com"
    ],

    "phonepe": [
        "phonepe.com"
    ],

    "ola": [
        "olacabs.com"
    ],

    "walmart": [
        "walmart.com"
    ],

    "linkedin": [
        "linkedin.com"
    ]
}


# ============================================================
# FIND OFFICIAL DOMAINS
# ============================================================

def get_official_domains(company_name):

    if not company_name:
        return []

    company = company_name.strip().lower()

    return OFFICIAL_DOMAINS.get(
        company,
        []
    )


# ============================================================
# CHECK WHETHER DOMAIN IS OFFICIAL
# ============================================================

def is_official_domain(
    company_name,
    submitted_domain
):

    official_domains = get_official_domains(
        company_name
    )

    if not official_domains:

        return {
            "status": "unknown",
            "message": (
                "Official domain is not available "
                "in the JobShield database."
            ),
            "official_domains": []
        }

    submitted_domain = (
        submitted_domain
        .strip()
        .lower()
        .replace("www.", "")
    )

    for official_domain in official_domains:

        official_domain = (
            official_domain
            .strip()
            .lower()
            .replace("www.", "")
        )

        # Exact domain
        if submitted_domain == official_domain:

            return {
                "status": "verified",
                "message": (
                    "The submitted domain matches "
                    "the company's official domain."
                ),
                "official_domains": official_domains
            }

        # Subdomain
        if submitted_domain.endswith(
            "." + official_domain
        ):

            return {
                "status": "verified",
                "message": (
                    "The submitted domain is a "
                    "subdomain of the company's "
                    "official domain."
                ),
                "official_domains": official_domains
            }

    return {
        "status": "not_verified",
        "message": (
            "The submitted domain does not match "
            "the company's registered official domain."
        ),
        "official_domains": official_domains
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("       JOBSHIELD OFFICIAL DOMAIN TEST")
    print("=" * 60)
    print()

    # Test 1
    result = is_official_domain(
        "Microsoft",
        "careers.microsoft.com"
    )

    print("Test 1:")
    print(result)

    print()

    # Test 2
    result = is_official_domain(
        "Microsoft",
        "microsoft-careers.example.com"
    )

    print("Test 2:")
    print(result)

    print()

    # Test 3
    result = is_official_domain(
        "Unknown Company",
        "example.com"
    )

    print("Test 3:")
    print(result)

    print()

    print("=" * 60)
    print("       OFFICIAL DOMAIN TEST COMPLETE")
    print("=" * 60)