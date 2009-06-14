def join_path(*args):
    """Join strings with / """
    s = []
    for i in args[:-1]:
        if not i:
            continue
        i = i.replace('\\', '/')
        if i.endswith('/'):
            s.append(i[:-1])
        else:
            s.append(i)
    s.append(args[-1])
    return '/'.join(s)