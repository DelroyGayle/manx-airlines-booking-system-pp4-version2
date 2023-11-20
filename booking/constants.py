"""
constants.py
Various Constants used throughout this App
"""

TITLE_CHOICES = [
        ("DR", "DOCTOR"),
        ("LADY", "LADY"),
        ("LORD", "LORD"),
        ("MSTR", "MASTER"),
        ("MISS", "MISS"),
        ("MR", "MR"),
        ("MRS", "MRS"),
        ("MS", "MS"),
        ("PROF", "PROFESSOR"),
        ("SIR", "SIR"),
        ("SIS", "SISTER"),
    ]

NULLPAX = "Enter the details for this passenger."
BAD_NAME = ("Names must begin and end with a letter. "
            "Names must consist of only alphabetical characters, "
            "apostrophes and hyphens.")
FIRSTNAME_BLANK = (f"Passenger Name required. "
                   f"Enter the First Name as on the passport.")
LASTNAME_BLANK = (f"Passenger Name required. "
                  f"Enter the Last Name as on the passport.")
CONTACTS_BLANK = ("Adult 1 is the Principal Passenger. "
                  "Contact Details are "
                  "mandatory for this Passenger. "
                  "Enter passenger's phone number and/or email.")
BAD_TELNO = "Enter a phone number of at least six digits."
BAD_EMAIL = "Enter a valid email address."
