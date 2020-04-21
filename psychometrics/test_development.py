import pandas as pd
import random

#todo Blueprint match

def build_parallel_forms(blueprint, items, forms_to_build):

    content_areas = blueprint.keys()
    sorted_list = sorted(items, key=lambda i: i['difficulty'])
    form_count = list(range(0, forms_to_build))
    empty_dict = {}
    for form in form_count:
        empty_dict['form' + str(form)]=[]


    items_for_forms = []
    for content_area in content_areas:
        items_from_area = blueprint[content_area]
        items_in_area = []
        for item in sorted_list:
            if item['content_area'] == content_area:
                items_in_area.append(item)

        items_zipped = list(zip(*(iter(items_in_area),) * forms_to_build))
        items_zipped = [list(elem) for elem in items_zipped]
        lr = random.sample(items_zipped, len(items_zipped))
        #items_for_forms.append(lr[0:items_from_area])
        lr = lr[0:items_from_area]
        shuffled_items = []
        for item_group in lr:
            shuffled = random.sample(item_group, len(item_group))
            shuffled_items.append(shuffled)
        #print(shuffled_items)


        for shuff in shuffled_items:
            #print(shuff)
            for form in form_count:
                empty_dict['form' + str(form)].append(shuff[form])
        #print(len(shuffled_items), shuffled_items)
    return empty_dict