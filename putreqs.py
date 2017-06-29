reqsput = {'create': 'INC'}

putfuncs = {'create': lambda x, y: create(x, y)}


def create(data, params):

    args = params.split(' ')
    new_url = reqsput[data[0]][:-3]
    for i in args:
        new_url +=  i + '/'
        print new_url
    new_url=new_url[:-1]
    return new_url


