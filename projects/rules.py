import rules

@rules.predicate
def is_project_user(user,education):
    return user == education.resume.user

def add_rule():
    rules.add_rule('is_project_user',is_project_user)