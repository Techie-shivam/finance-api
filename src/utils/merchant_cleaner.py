import re


def clean_merchant(text):

    text = text.upper()

    text = re.sub(
        r"[^A-Z ]",
        "",
        text
    )

    return text.strip()