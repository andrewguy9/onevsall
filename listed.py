from join_csv import table

def get_item_iter(path):
    items = table(path)
    for item in items.dict_cursor():
        yield item

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
