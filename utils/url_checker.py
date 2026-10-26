# ============================================================
# JOBSHIELD - URL CHECKER
# ============================================================

import requests

from urllib.parse import urlparse


# ============================================================
# EXTRACT DOMAIN
# ============================================================

def extract_domain(url):

    if not url:
        return None

    url = url.strip()

    # Add HTTPS if no protocol was provided
    if not url.startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    try:

        parsed_url = urlparse(url)

        domain = parsed_url.netloc.lower()

        # Remove username/password
        if "@" in domain:
            domain = domain.split("@")[-1]

        # Remove port
        domain = domain.split(":")[0]

        # Remove www
        if domain.startswith("www."):
            domain = domain[4:]

        if not domain:
            return None

        return domain

    except Exception:

        return None


# ============================================================
# VALIDATE URL FORMAT
# ============================================================

def validate_url(url):

    if not url:

        return {
            "valid": False,
            "domain": None,
            "message": "URL is empty."
        }

    domain = extract_domain(url)

    if not domain:

        return {
            "valid": False,
            "domain": None,
            "message": "Invalid URL."
        }

    return {
        "valid": True,
        "domain": domain,
        "message": "URL format is valid."
    }


# ============================================================
# CHECK WEBSITE ACCESSIBILITY
# ============================================================

def check_website(url):

    if not url:

        return {
            "accessible": False,
            "status_code": None,
            "https": False,
            "final_url": None,
            "final_domain": None,
            "redirected": False,
            "message": "URL is empty."
        }

    original_url = url.strip()

    # Add HTTPS if protocol is missing
    if not original_url.startswith(
        ("http://", "https://")
    ):

        original_url = (
            "https://" + original_url
        )

    parsed = urlparse(
        original_url
    )

    https_enabled = (
        parsed.scheme.lower() == "https"
    )

    try:

        response = requests.get(
            original_url,
            timeout=10,
            allow_redirects=True,
            headers={
                "User-Agent":
                "JobShield-URL-Checker/1.0"
            }
        )

        final_url = response.url

        final_domain = extract_domain(
            final_url
        )

        redirected = (
            final_url.rstrip("/")
            != original_url.rstrip("/")
        )

        return {

            "accessible": True,

            "status_code": response.status_code,

            "https": https_enabled,

            "final_url": final_url,

            "final_domain": final_domain,

            "redirected": redirected,

            "message": (
                "Website is accessible."
            )
        }

    except requests.exceptions.SSLError:

        return {

            "accessible": False,

            "status_code": None,

            "https": https_enabled,

            "final_url": None,

            "final_domain": None,

            "redirected": False,

            "message": (
                "SSL certificate verification failed."
            )
        }

    except requests.exceptions.Timeout:

        return {

            "accessible": False,

            "status_code": None,

            "https": https_enabled,

            "final_url": None,

            "final_domain": None,

            "redirected": False,

            "message": (
                "Website request timed out."
            )
        }

    except requests.exceptions.ConnectionError:

        return {

            "accessible": False,

            "status_code": None,

            "https": https_enabled,

            "final_url": None,

            "final_domain": None,

            "redirected": False,

            "message": (
                "Unable to connect to the website."
            )
        }

    except requests.exceptions.RequestException as e:

        return {

            "accessible": False,

            "status_code": None,

            "https": https_enabled,

            "final_url": None,

            "final_domain": None,

            "redirected": False,

            "message": (
                f"Website request failed: {str(e)}"
            )
        }


# ============================================================
# COMPLETE URL CHECK
# ============================================================

def check_url(url):

    validation = validate_url(
        url
    )

    if not validation["valid"]:

        return {
            "valid": False,
            "domain": None,
            "accessible": False,
            "status_code": None,
            "https": False,
            "final_url": None,
            "final_domain": None,
            "redirected": False,
            "message": validation["message"]
        }

    website = check_website(
        url
    )

    return {

        "valid": True,

        "domain": validation[
            "domain"
        ],

        "accessible": website[
            "accessible"
        ],

        "status_code": website[
            "status_code"
        ],

        "https": website[
            "https"
        ],

        "final_url": website[
            "final_url"
        ],

        "final_domain": website[
            "final_domain"
        ],

        "redirected": website[
            "redirected"
        ],

        "message": website[
            "message"
        ]
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()

    print("=" * 60)
    print("       JOBSHIELD URL CHECKER TEST")
    print("=" * 60)

    print()

    test_urls = [

        "https://www.google.com",

        "https://www.microsoft.com",

        "https://careers.microsoft.com",

        "https://this-website-does-not-exist-12345.com"
    ]

    for url in test_urls:

        print(
            f"URL: {url}"
        )

        result = check_url(
            url
        )

        print(
            f"Valid: {result['valid']}"
        )

        print(
            f"Domain: {result['domain']}"
        )

        print(
            f"Accessible: {result['accessible']}"
        )

        print(
            f"Status Code: {result['status_code']}"
        )

        print(
            f"HTTPS: {result['https']}"
        )

        print(
            f"Final URL: {result['final_url']}"
        )

        print(
            f"Final Domain: {result['final_domain']}"
        )

        print(
            f"Redirected: {result['redirected']}"
        )

        print(
            f"Message: {result['message']}"
        )

        print("-" * 60)

    print()

    print("=" * 60)
    print("       URL CHECKER TEST COMPLETE")
    print("=" * 60)