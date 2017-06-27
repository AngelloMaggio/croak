deletereqs = { 'deleteuser' : 'api/security/users/INC'}

deletefuncs = { 'deleteuser': lambda x,y : deleteuser(x,y)}

def deleteuser(data, oArgs):
    if oArgs == 'INC':
        new_url = deletereqs[data[0]][:-3] + data[1]
        print 'here inside delete'
        return new_url

    else:
        out =''
        print 'doing the else'
        return 'The User not found'


