delete_requests = {'delete_user': 'api/security/users/INC'}

delete_functions = {'delete_user': lambda x, y: delete_user(x, y)}


def delete_user(data, params):

    new_url = delete_requests[data[0]][:-3] + data[1]
    print 'here inside delete'
    return new_url


