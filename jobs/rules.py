import rules

@rules.predicate
def is_company(custom_user):
    return custom_user.user_type == 2

@rules.predicate
def is_current_company(user,company):
    return user == company.custom_user


rules.add_perm('jobs.show_job',is_company)
rules.add_rule('is_current_company',is_current_company)