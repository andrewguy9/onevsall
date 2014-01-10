def flatten(ii):
    for i in ii:
        for e in i:
            yield e

def tail(c):
    i = iter(c)
    i.next()
    for e in i:
        yield e

def head(c):
    i = iter(c)
    yield i.next()
