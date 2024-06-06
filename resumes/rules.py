import rules


@rules.predicate
def is_resume_user(resume_user,resume):
    return resume_user == resume.user


def add_rule():
    rules.add_rule('is_resume_user',is_resume_user)

add_rule()
