from join_csv import file_table

def get_item_iter(path):
    items = file_table(path)
    for item in items.dict_cursor():
        yield item
