reqspost = {'makebundle': 'api/support/bundles'}

postfuncs = {'makebundle': lambda x, y: makebundle(x, y)}

def makebundle(data, oArgs):
    return str(data)
