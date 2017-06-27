reqsput = {'create':'INC'}

putfuncs = {'create': lambda x, y: create(x, y)}

def create(data, oArgs):
    print "inside create function"
    if oArgs == 'INC':
        new_url = reqsput[data[0]][:-3] + data[1] + '/' + data[2]
        return new_url
    else:
        return str(data)


