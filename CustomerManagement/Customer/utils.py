from datetime import date


def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year

    # Check if the birthday has already occurred this year
    if today.month < date_of_birth.month or (today.month == date_of_birth.month and today.day < date_of_birth.day):
        age -= 1

    return age
