import rules

@rules.predicate
def is_company(custom_user):
    return custom_user.user_type == 2


rules.add_perm('jobs.show_job',is_company)