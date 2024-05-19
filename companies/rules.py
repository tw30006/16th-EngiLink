import rules

@rules.predicate
def is_company(custom_user):
    return custom_user.user_type == 2

@rules.predicate
def is_user(custom_user):
    return custom_user.user_type == 1

rules.add_perm('companies.detail_company',is_company)
rules.add_perm('companies.home_company',is_company)