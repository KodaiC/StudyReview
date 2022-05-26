import rules


@rules.predicate
def is_rater_or_admin(user, rating):
    return rating.rater == user


rules.add_perm("api.change_rating", is_rater_or_admin)
rules.add_perm("api.delete_rating", is_rater_or_admin)
rules.add_perm("api.add_rating", rules.is_active)

rules.add_perm("api.add_tag", rules.is_active)
