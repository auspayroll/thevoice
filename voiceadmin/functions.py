def in_group(group_name):
	if not isinstance(group_name, list):
		group_name = [group_name]
	return lambda user: user.groups.filter(name__in=group_name).count() > 0

def is_member(user, group):
    return user.groups.filter(name=group).exists()

def update_average(average=0, n=0, value=0):
	return (round(((average or 0) * n + value) / (n+ 1),2) , n+1)

