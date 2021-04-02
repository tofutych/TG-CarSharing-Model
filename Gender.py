class Gender(object):
    genders = ["male", "female"]

    def __init__(self, gender):
        if gender.lower() not in Gender.genders:
            Gender.genders.append(gender.lower())

    @classmethod
    def all(cls):
        return Gender.genders