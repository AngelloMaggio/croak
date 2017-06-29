reqsget = {'repos': 'api/repositories',
           'storage': 'api/storageinfo',
           'tasks': 'api/tasks',
           'replication': 'api/replications/INC',
           'user': 'api/security/users/INC',
           'listbundles': 'api/support/bundles',
           'getbundle': 'api/support/bundles/INC',
           'license': 'api/system/license',
           'build': 'api/build/INC'
           }

getfuncs = {'repos': lambda x, y, z: repos(x, y, z),
            'storage': lambda x, y, z: storage(x, y, z),
            'tasks': lambda x, y, z: tasks(x, y, z),
            'replication': lambda x, y, z: replication(x, y, z),
            'user': lambda x, y, z: user(x, y, z),
            'listbundles': lambda x, y, z: listbundles(x,y,z),
            'getbundle': lambda x, y, z: getbundle(x, y, z),
            'license': lambda  x,y,z : license(x,y,z),
            'build' : lambda  x,y,z : build(x,y,z),
            }


# Handles a couple of the build calls since they share a pretty big part of the api URL
def build(data, params, inc):

    if inc:
        args = params.split(' ')

        if len(args) == 3:
            args = args[:-1] + ['?diff=' + args[-1]]

        new_url = reqsget[data[0]][:-3]
        for i in args:
            new_url += i + '/'
            print new_url
        new_url=new_url[:-1]
        return new_url

    else:
        out = ''
        if data['errors'] != '':
            for item in data['errors']:
                out += '<br \>' + str(item['status'])
        elif data['builds'] != '':
            for item in data['builds']:
                out += '<br \>' + 'Uri:' + item['uri'] + 'last Started :' + item['lastStarted']

    return out



def license(data, params, inc):   #Check License
    out = ''
    out += '<br>' + data['type']
    out += '<br>' + data['validThrough']
    out += '<br>' + data['licensedTo']
    return out


def repos(data, params, inc):     #Check Repos
    out = ''
    for item in data:
        out += "<br />" + item['key']
    return out


def storage(data, params, inc):   #Check Storage of the Instance

    fs_data = data['fileStoreSummary']

    bin_sum = data['binariesSummary']

    return "Your Storage Directory is located at " + fs_data['storageDirectory'] + '<br \>' + \
           "You have " + fs_data['freeSpace'] + " of free space, <br \> having used " + fs_data['usedSpace'] + " of the total " + fs_data['totalSpace'] +\
           "<br \>You have" + bin_sum['artifactsCount'] + " artifacts, that use " + bin_sum['artifactsSize'] + ' of your disk.' +\
           "<br \>You have" + bin_sum['binariesCount'] + " binaries, <br \>that use " + bin_sum['binariesSize'] + 'of your disk.' +\
           "<br \>Your Storage Directory is located at" + fs_data['storageDirectory'] + '<br>' + \
           "You have" + fs_data['freeSpace'] + "of free space, having used" + fs_data['usedSpace'] + "of the total" + fs_data['totalSpace']


def replication(data, params, inc):

    if inc:
        new_url = reqsget[data[0]][:-3] + params
        return new_url

    else:
        out = ''
        for item in data:

            out += item['repoKey'], 'for user', item['username'], "with cron expression", item['cronExp'] + '<br>'

            if params[1] == 'plus':
                out += '<br>' "Sync Statistics: " + item['syncStatistics'] + " Sync Deletes:" + \
                       item['syncDeletes'] + "Timeout: " + item['socketTimeoutMillis']
                out += '<br>'

        return out


def user(data, params, inc):    #List the Users

    if inc:
        new_url = reqsget[data[0]][:-3] + params
        return new_url
    else:
        return "User " + data['name'], " was last seen online ", data['lastLoggedIn']


def tasks(data, params, inc):  #List the Background Tasks
    out = ''
    for task in data['tasks']:

        out += task['id'] + ' : ' + task['description'] + '<br>'
        if params[0] == 'plus':
            out += task['state'] + 'Type:' + task['type'] + '<br>'
        out+= "--o--\n"
    return out

def listbundles(data, params, inc):
    return str(data)

def getbundle(data, params, inc):
    if inc:
        new_url = reqsget[data[0]][:-3] + data[1]
        return new_url
    else:
        return str(data)




