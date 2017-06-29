deletereqs = { 'deleteuser' : 'api/security/users/INC'}

deletefuncs = { 'deleteuser': lambda x,y : deleteuser(x,y)}

def deleteuser(data, params):
    if params == 'INC':
        new_url = deletereqs[data[0]][:-3] + data[1]
        print 'here inside delete'
        return new_url

    else:
        out = ''
        out += str(data)
        return out


