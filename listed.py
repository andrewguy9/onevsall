from join_csv import table

def get_item_iter(path):
    items = table(path)
    for item in items.dict_cursor():
        yield item
