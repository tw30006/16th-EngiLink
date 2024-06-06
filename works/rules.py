import rules


@rules.predicate
def is_work_user(user,resume):
    return user == resume.user


def add_rule():
    rules.add_rule("is_work_user", is_work_user)
