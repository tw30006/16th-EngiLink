import rules

@rules.predicate
def is_company(custom_user):
    return custom_user.is_authenticated and custom_user.user_type == 2


rules.add_perm('company_can_show',is_company)