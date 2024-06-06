import rules


@rules.predicate
def is_user(custom_user):
    return custom_user.is_authenticated and custom_user.user_type == 1


rules.add_perm("user_can_show", is_user)
