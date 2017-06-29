post_requests = {'make_bundle': 'api/support/bundles',
                 'optimize_storage': 'api/system/storage/optimize',
                 'build_promote': 'api/build/promote/INC',
                 'docker_promote': 'api/docker/INC',
                 'build_rename': 'api/build/rename/INC'}

post_functions = {'build_promote': lambda x, y: build_promote(x, y),
                  'docker_promote': lambda x, y: docker_promote(x, y),
                  'build_rename': lambda x, y: build_rename(x, y)}


def build_rename(data, params):

    args = params.split(' ')
    new_url = post_requests[data[0]][:-3] + '/' + args[0] + '/' + args[1]
    return new_url


def docker_promote(data, params):

    new_url = post_requests[data[0]][:-3] + '/' + params + '/v2/promote'
    return new_url


def build_promote(data, params):

    args = params.split(' ')
    new_url = post_requests[data[0]][:-3] + '/' + args[0] + '/' + args[1]
    return new_url
