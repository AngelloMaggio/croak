reqsput = {'mkdir': 'INC'}

putfuncs = {'mkdir': lambda x, y: mkdir(x, y)}

def mkdir(data, oArgs):
    print "inside mkdir function"
    if oArgs == 'INC':
        new_url = reqsput[data[0]][:-3] + data[1] + '/' + data[2]
        return new_url
    else:
        print str(data)
        return str(data)
