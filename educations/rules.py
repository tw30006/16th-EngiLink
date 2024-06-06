import rules


@rules.predicate
def is_education_user(user,resume):
    return user == resume.user

def add_rule():
    rules.add_rule("is_education_user", is_education_user)
