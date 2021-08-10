import elabapy
import json
import pandas as pd
from datetime import date
import os

# Put YOUR variables here:
# the annotation file should be a Excel file (.xlsx or +.xls format, e.g. "C:\\Users\\\Default\\Documents\\RDM4mic.xlsx")
annotation_file = os.path.abspath("Annotation_example.xlsx")
# replace the token with your generated API key, which is only showed once!
my_token = "b4af0c08363734890f1811436a1c7d6355d6a9e8d0923f77cd4f3c4a062db09093adfaa3c79e574520cc"
# the title of your new database
new_title = "API_example"



def elab_items_demo(manager):
    # the elab_items_demo function shows your entries in eLabFTW
    items_types = manager.get_all_items()
    print(json.dumps(items_types, indent=4, sort_keys=True))
    # get all experiments
    all_exp = manager.get_all_experiments()
    print(json.dumps(all_exp, indent=4, sort_keys=True))
    # get item with id 1
    #item = manager.get_item(1)
    #print(json.dumps(item, indent=4, sort_keys=True))

def elab_create_database(manager):
    '''the elab_create_database function looks for database categories and creates a empty database with a randomly assigned category'''
    items_types = manager.get_items_types()
    #print(json.dumps(items_types, indent=4, sort_keys=True))
    first_category = items_types[0]["category_id"]
    response = manager.create_item(first_category)
    print(f"Created database item with id {response['id']}.")
    return response['id']

def read_annotation(annotation_file,id,manager):
    # import Excel files
    dict_from_file = pd.read_excel(annotation_file).to_dict()

    ## if you prefer csv files, please un/comment accordingly
    # with open(annotation_file, "r", encoding="utf-8") as infile:
    #     dict_from_csv = pd.read_csv(annotation_file, sep=";",header=0, index_col=False,squeeze=True).to_dict()
    #     print(dict_from_file)
    return dict_from_file

def update_database(manager, id,csv_dict_import,new_title):
    # put the imported file in the body of an eLabFTW database
    body_text = ""
    for key in csv_dict_import:
        body_text = body_text + str(key) + " : "
        for i in range(0,len(csv_dict_import[key])):
            if i == 0:
                tmp_text = ""
            else:
                tmp_text = ", "
            body_text = body_text + tmp_text + str(csv_dict_import[key][i])
            i+=1
        body_text = body_text + "<br>\n"
    today = date.today().strftime("%Y%m%d")
    params = {"title": new_title,"date": today, "body": body_text}
    print(manager.post_item(id, params))

if __name__ == '__main__':
    # call diverse functions of the main program
    manager = elabapy.Manager(endpoint="https://elabftw.hhu.de/api/v1/", token=my_token, verify=False)

    ## comment/uncomment functions with '#'

    elab_items_demo(manager)
    id = elab_create_database(manager)
    csv_dict_import = read_annotation(annotation_file,id,manager)
    update_database(manager, id, csv_dict_import, new_title)




