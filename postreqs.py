reqspost = {'makebundle': 'api/support/bundles',
            'optimizestorage' : 'api/system/storage/optimize',
           'build_promote': 'api/build/promote/INC',
            'docker_promote': 'api/docker/INC',
            'build_rename': 'api/build/rename/INC'}

postfuncs = {'makebundle': lambda x, y: makebundle(x, y),
             'optimizestorage' : lambda x, y: optimizestorage(x,y),
             'build_promote': lambda x,y,z: buildpromote(x,y,z),
             'docker_promote': lambda x,y,z: dockerpromote(x,y,z),
             'build_rename': lambda x, y, z: buildrename(x,y,z)}


def buildrename(data, params, inc):

    if inc:

        args = params.split(' ')

        new_url = reqspost[data[0]][:-3] + '/' + args[0] + '/' + args[1]

        return new_url
    else:
        out = str(data)
        return out


def dockerpromote(data, params, inc):

    if inc:



        new_url = reqspost[data[0]][:-3] + '/' + params + '/v2/promote'

        return new_url

    else:
        out = str(data)

        return out

def optimizestorage(data, params, inc):
    return str(data)

def makebundle(data, params, inc):
    return str(data)

def buildpromote(data, params, inc):

    if inc:
        args = params.split(' ')
        new_url = reqspost[data[0]][:-3] + '/' + args[0] + '/' + args[1]

        return new_url

    else:
        out = str(data)

    return out
