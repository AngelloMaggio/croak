# Dictionary with base url's for API calls
get_requests = {'repositories': 'api/repositories',
                'storage': 'api/storageinfo',
                'tasks': 'api/tasks',
                'replication': 'api/replications/INC',
                'user': 'api/security/users/INC',
                'list_bundles': 'api/support/bundles',
                'get_bundle': 'api/support/bundles/INC',
                'license': 'api/system/license',
                'build': 'api/build/INC',
                'folder_info': 'api/storage/INC',
                'file_info': 'api/storage/INC'
                }

# Dictionary of functions to handle more complex api urls
get_functions = {
            'replication': lambda x, y: replication(x, y),
            'user': lambda x, y: user(x, y),
            'get_bundle': lambda x, y: get_bundle(x, y),
            'license': lambda x, y: license(x, y),
            'build': lambda x, y: build(x, y),
            'folder_info': lambda x, y: file_folder_info(x, y),
            'file_info': lambda x, y: file_folder_info(x, y),
            }


def file_folder_info(data, params):

    args = params.split(' ')
    new_url = get_requests[data[0]][:-3] + args[0] + '/' + args[1]

    if data[0] == 'folderinfo':
        new_url += '/'

    return new_url


# Handles a couple of the build calls since they share a pretty big part of the api URL
def build(data, params):

    args = params.split(' ')

    if len(args) == 3:
        args = args[:-1] + ['?diff=' + args[-1]]

    new_url = get_requests[data[0]][:-3]
    for i in args:
        new_url += i + '/'
        print new_url
    new_url = new_url[:-1]

    return new_url


def replication(data, params):

    new_url = get_requests[data[0]][:-3] + params
    return new_url


def user(data, params):    #List the Users

    new_url = get_requests[data[0]][:-3] + params
    return new_url


def get_bundle(data, params):

    new_url = get_requests[data[0]][:-3] + params
    return new_url




