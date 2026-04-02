import re

def clean_data(data):
    email = data.get("email")
    if email and not re.match(r"[\w.-]+@[\w.-]+\.\w{2,}", email):
        data["email"] = None
    phone = data.get("phone")
    if phone and not re.match(r"\+?\d[\d\s-]{8,15}", phone):
        data["phone"] = None
    return data