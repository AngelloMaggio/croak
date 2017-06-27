reqspost = {'makebundle': 'api/support/bundles',
            'optimizestorage' : 'api/system/storage/optimize'}

postfuncs = {'makebundle': lambda x, y: makebundle(x, y),
             'optimizestorage' : lambda x, y: optimizestorage(x,y)}



def optimizestorage(data, oArgs):
    return str(data)

def makebundle(data, oArgs):
    return str(data)