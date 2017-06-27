reqsget = {'repos': 'api/repositories',
        'storage': 'api/storageinfo',
        'tasks': 'api/tasks',
        'replication': 'api/replications/INC',
        'user': 'api/security/users/INC',
        'listbundles': 'api/support/bundles',
        'getbundle': 'api/support/bundles/INC',
        'license': 'api/system/license',
        'build': 'api/build'
           }

getfuncs = {'repos': lambda x, y: repos(x, y),
            'storage': lambda x, y: storage(x, y),
            'tasks': lambda x, y: tasks(x, y),
            'replication': lambda x, y: replication(x, y),
            'user': lambda x, y: user(x, y),
            'listbundles': lambda x, y: listbundles(x,y),
            'getbundle': lambda x, y: getbundle(x, y),
            'license': lambda  x,y : license(x,y),
            'build' : lambda  x,y : build(x,y)
            }

def build(data, oArgs):
    out = ''
    if data['errors'] != '':
        for item in data['errors']:
            out += '\n' + str(item['status'])
    elif data['builds'] != '':
        for item in data['builds']:
            out += '\n' + 'Uri:' + item['uri'] + 'last Started :' + item['lastStarted']
    return out




def license(data, oArgs):   #Check License
    out = ''
    out += '<br>' + data['type']
    out += '<br>' + data['validThrough']
    out += '<br>' + data['licensedTo']
    return out

def repos(data, oArgs):     #Check Repos
    out = ''
    for item in data:
        out += "<br />" + item['key']
    return out
def storage(data, oArgs):   #Check Storage of the Instance
    fs_data = data['fileStoreSummary']

    if oArgs[0] == 'plus':
        bin_sum = data['binariesSummary']

        return "Your Storage Directory is located at " + fs_data['storageDirectory'] + '<br>' + \
            "You have " + fs_data['freeSpace'] + " of free space, \n having used " + fs_data['usedSpace'] + " of the total " + fs_data['totalSpace'] +\
            "\nYou have" + bin_sum['artifactsCount'] + " artifacts, that use " + bin_sum['artifactsSize'] + ' of your disk.' +\
            "\nYou have" + bin_sum['binariesCount'] + " binaries, \nthat use " + bin_sum['binariesSize'] + 'of your disk.'
    else:
        return "Your Storage Directory is located at" + fs_data['storageDirectory'] + '<br>' + \
             "You have" + fs_data['freeSpace'] + "of free space, having used" + fs_data['usedSpace'] + "of the total" + fs_data['totalSpace']


def replication(data, oArgs):
    if oArgs == 'INC':
        new_url = reqsget[data[0]][:-3] + data[1]
        return new_url

    else:
        out = ''
        for item in data:

            out += item['repoKey'], 'for user', item['username'], "with cron expression", item['cronExp'] + '<br>'

            if oArgs[1] == 'plus':
                out += '<br>' "Sync Statistics: " + item['syncStatistics'] + " Sync Deletes:" + \
                       item['syncDeletes'] + "Timeout: " + item['socketTimeoutMillis']
                out += '<br>'
        return out


def user(data, oArgs):    #List the Users
    if oArgs == 'INC':
        new_url = reqsget[data[0]][:-3] + data[1]
        return new_url
    else:
        return "User " + data['name'], " was last seen online ", data['lastLoggedIn']


def tasks(data, oArgs):  #List the Background Tasks
    out = ''
    for task in data['tasks']:

        out += task['id'] + ' : ' + task['description'] + '<br>'
        if oArgs[0] == 'plus':
            out += task['state'] + 'Type:' + task['type'] + '<br>'
        out+= "--o--\n"
    return out

def listbundles(data, oArgs):
    return str(data)

def getbundle(data, oArgs):
    if oArgs == 'INC':
        new_url = reqsget[data[0]][:-3] + data[1]
        return new_url
    else:
        return str(data)




