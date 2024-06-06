import rules


@rules.predicate
def is_project_user(user,resume):
    return user == resume.user


def add_rule():
    rules.add_rule("is_project_user", is_project_user)
