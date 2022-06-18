def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """
    resulting_path = []
    root = '/' if path and path[0] == '/' else ''
    for pwd in path.split('/'):
        if pwd == '.' or pwd == '':
            continue
        elif not pwd == '..':
            resulting_path.append(pwd)
            continue
        elif not root and (not resulting_path or resulting_path[-1] == '..'):
            resulting_path.append(pwd)
        elif resulting_path:
            resulting_path.pop()
    a = root + '/'.join(x for x in resulting_path)
    return a if a else '.'

