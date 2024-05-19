import rules

@rules.predicate
def is_company(custom_user):
    return custom_user.user_type == 2

@rules.predicate
def is_user(custom_user):
    return custom_user.user_type == 1


rules.add_perm('resumes.show_job',is_user)