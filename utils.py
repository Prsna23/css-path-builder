from bs4 import Tag

def childElementCount(node):
    siblingNodes = [elem for elem in list(node.previous_siblings) if isinstance(elem, Tag)]
    return len(siblingNodes)

def getUniqueCssPath(node):
    siblingNodes = getSiblings(node)
    count = 0
    for sibling in siblingNodes:
        if(isinstance(sibling, Tag) and sibling.name.lower() == node.name.lower()):
            count += 1
    if(count == 1): 
        return ""
    count = 0
    if 'class' in node.attrs:
        nodeClassName = node.name.lower() + '.' + '.'.join(node['class'])
        for sibling in siblingNodes:
            siblingNodeName = ""
            if 'class' in sibling.attrs:
                siblingNodeName = sibling.name.lower() + '.' + '.'.join(sibling['class'])
            else: siblingNodeName = sibling.name.lower()
            if(nodeClassName == siblingNodeName): count+=1
        if(count == 1): return '.' + '.'.join(node['class'])
    
    return ":nth-child(" + str(childElementCount(node) + 1) + ")"


def recursiveNodes(node):
    n = []
    if(node.name and node.parent and node.name.lower() != "body"):
        n = recursiveNodes(node.parent)
    n.append(node)
    return n

def getCssPath(node):
    nodes = recursiveNodes(node)
    path = ""
    for node in nodes:
        if(node):
            if 'id' in node.attrs:
                path += '#' + node['id']
            else: 
                path += node.name.lower()
                path += getUniqueCssPath(node)
            path += " > "

    if path[-3:] == " > ":
        return path[: -3]
    return path

def getSiblings(node): 
    siblingNodes = list(node.previous_siblings) + list(node.next_siblings)
    siblingNodes.append(node)
    siblingNodes = [elem for elem in siblingNodes if isinstance(elem, Tag)]
    return siblingNodes

def getParent(node): 
    return node.parent



