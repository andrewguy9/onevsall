from csv import reader

def get_item_iter(path):
    f = open(path, 'r')
    r = reader(f)
    items = tail(r)
    for item in items:
        (id, title, description, price) = item
        d = {'id':id, 'title':title, 'description':description, 'price':price}
        yield d

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
