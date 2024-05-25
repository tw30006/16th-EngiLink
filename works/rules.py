import rules

@rules.predicate
def is_work_user(user,work):
    return user == work.resume.user

def add_rule():
    rules.add_rule('is_work_user',is_work_user)