import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Add it to your .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=60000
    )
)


# ============================================================
# CODE REVIEW
# ============================================================

def review_code(code, review_depth="Deep Review"):

    if not code or not code.strip():
        return {
            "status": "ERROR",
            "message": "Please enter some code."
        }

    # --------------------------------------------------------
    # REVIEW TYPE
    # --------------------------------------------------------

    if review_depth == "Quick Scan":

        focus = """
Focus mainly on:
- Major bugs
- Security issues
- Readability
- Obvious performance problems
- Important improvements
"""

    else:

        focus = """
Perform a detailed professional code review.

Analyze:
- Bugs
- Edge cases
- Security vulnerabilities
- Performance
- Readability
- Maintainability
- Code smells
- Complexity
- Error handling
- Refactoring opportunities
"""

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are CodeSense, an expert senior software engineer.

Review the following source code.

{focus}

SOURCE CODE
==================================================

{code}

==================================================

IMPORTANT INSTRUCTIONS

1. Determine whether the input is actually programming code.

2. If it is NOT programming code, return exactly:

NOT_CODE

3. If it IS programming code, provide a professional review.

4. Do not invent bugs.

5. Line numbers must correspond to the supplied code.

6. Keep explanations simple and understandable.

7. Preserve the original functionality when refactoring.

Use the following format:

LANGUAGE
<detected language>

SUMMARY
<simple explanation of what the code does>

BUGS
<list actual bugs>

If there are no bugs:
No major bugs detected.

SECURITY
<list genuine security issues>

If there are no security issues:
No major security vulnerabilities detected.

PERFORMANCE
<list important performance problems>

If there are no important performance problems:
No major performance issues detected.

COMPLEXITY

Time Complexity:
<complexity>

Space Complexity:
<complexity>

Explanation:
<why>

READABILITY

Score:
<number>/10

Explanation:
<reason>

CODE QUALITY

Discuss:
- Naming
- Structure
- Maintainability
- Error handling
- Best practices

REFACTORING NOTES

<practical improvements>

REFACTORED CODE

<complete improved code>

END REVIEW
"""

    # --------------------------------------------------------
    # GEMINI REQUEST
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=4000
            )
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        if not response.text:

            return {
                "status": "ERROR",
                "message": "Gemini returned an empty response."
            }

        result = response.text.strip()

        if result == "NOT_CODE":

            return {
                "status": "NOT_CODE"
            }

        return {
            "status": "SUCCESS",
            "review": result
        }

    except Exception as e:

        return {
            "status": "ERROR",
            "message": str(e)
        }


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    test_code = """
def calculate_average(numbers):

    total = 0

    for number in numbers:
        total += number

    return total / len(numbers)


numbers = [10, 20, 30, 40]

print(calculate_average(numbers))
"""

    print()
    print("=" * 60)
    print("                 CODESENSE")
    print("=" * 60)
    print()

    result = review_code(
        test_code,
        "Deep Review"
    )

    if result["status"] == "SUCCESS":

        print(result["review"])

    elif result["status"] == "NOT_CODE":

        print("The provided input is not programming code.")

    else:

        print("ERROR:")
        print(result["message"])

    print()
    print("=" * 60)
# AI-powered code reviewer    