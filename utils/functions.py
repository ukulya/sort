def clean_phone_number(phone: str):
    if phone:
        return phone.replace('(', '').replace(')', '').replace('-', '')
    return phone
