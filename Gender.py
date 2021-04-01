class Gender(object):
    genders = ['male', 'female']

    def __init__(self, gender):
        if gender not in Gender.genders:
            Gender.genders.append(gender)

    @classmethod
    def all(cls):
        return Gender.genders