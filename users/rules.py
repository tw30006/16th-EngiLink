import rules

@rules.predicate
def is_user(custom_user):
    if not custom_user.is_authenticated:
        return False
    return custom_user.user_type == 1


rules.add_perm('user_can_show',is_user)