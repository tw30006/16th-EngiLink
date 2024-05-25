import rules


@rules.predicate
def is_resume_user(user,resume):
    return user == resume.user

def add_rule():
    rules.add_rule('is_resume_user',is_resume_user)
