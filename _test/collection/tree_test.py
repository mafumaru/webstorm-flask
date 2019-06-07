import json

cursor = [
    {'text':'收藏1','id':1,'parentid':0},
    {'text':'收藏2','id':2,'parentid':0},
    {'text':'收藏3','id':3,'parentid':1},
    {'text':'收藏4','id':4,'parentid':1},
    {'text':'收藏5','id':5,'parentid':3},
    {'text':'收藏6','id':6,'parentid':2},
    {'text':'收藏7','id':7,'parentid':6}
]

def list_to_tree(listdata):
    tree = []
    for treenode in listdata:
        if treenode['parentid']==0:
            tree.append(treenode)
        for it in listdata:
            if it['parentid'] == treenode['id']:
                if 'node' not in treenode.keys():
                    treenode['nodes']=[]
                treenode['nodes'].append(it)
    return tree

tree = list_to_tree(cursor)
treedata = json.dumps(tree)
print('')