reqsput = {'create':'INC'}

putfuncs = {'create': lambda x, y, z: create(x, y, z)}

def create(data, oArgs, inc):
    print "inside create function"

    if inc:
        args = oArgs.split(' ')
        new_url = reqsput[data[0]][:-3]
        for i in args:
            new_url +=  i + '/'
            print new_url
        new_url=new_url[:-1]
        return new_url
    else:
        return str(data)


