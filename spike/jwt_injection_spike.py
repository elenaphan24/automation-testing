"""JWT injection spike checklist.

Run against the real sandbox SUT before any production E2E flow depends on token
injection. This file intentionally documents the experiment boundary; it avoids
pretending the greenfield fake SUT can answer security questions about the app.
"""


QUESTIONS = [
    "Can a Playwright BrowserContext accept a JWT from the API response?",
    "Does the app enforce CSRF validation on injected sessions?",
    "What is the token TTL, and can it expire mid-suite?",
    "Does session binding prevent cross-environment injection?",
]


def main() -> None:
    for index, question in enumerate(QUESTIONS, start=1):
        print(f"{index}. {question}")


if __name__ == "__main__":
    main()

