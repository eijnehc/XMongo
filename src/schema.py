def nested_dict_all_key_path_ver2(path, nested_dict, lst_output=[]):
    for k, v in nested_dict.items():
        if isinstance(v , dict):
            nested_dict_all_key_path_ver2 (path + "." + k , v, lst_output)
        elif isinstance(v, list):
            path = path + "." + k
            for nested_dict_in_array in v:   
                if type(nested_dict_in_array) != str:      
                    for k1, v1 in nested_dict_in_array.items():
                        if isinstance(v1 , dict):
                            nested_dict_all_key_path_ver2 (path + "." + k1 , v1, lst_output)
                        else:
                            lst_output.append(path + "." + k1)
                else:
                    lst_output.append(path)     
        else:
            #print (path+"."+k,"=>",v)
            #print (path + "."+ k)
            lst_output.append(path + "."+ k)
    return lst_output

def remove_first_dot_input_lst_of_lst(lst_of_lst):
    for index_i, lst_i in enumerate(lst_of_lst):
        for index_j, value_j in enumerate(lst_i):
            lst_of_lst[index_i][index_j] = value_j[1:]
    return lst_of_lst

# The assumption here is the fixed schema that we talk about, each document by right should have the same key paths.
# So we just take the first document and cross check if our xpath_construct_db is INSIDE one of the path.
def get_atlas_schema(collection): 
    all_documents_in_1_collection = collection.find()
    lst_of_dict_collection = list(all_documents_in_1_collection)

    out = []

    for index, doc in enumerate(lst_of_dict_collection):
        out.append(nested_dict_all_key_path_ver2("", lst_of_dict_collection[index], []))

    return list(set(remove_first_dot_input_lst_of_lst(out)[0]))

def get_schema(collection): 
    lst_of_dict_collection = list(collection)

    out = []

    for index, doc in enumerate(lst_of_dict_collection):
        out.append(nested_dict_all_key_path_ver2("", lst_of_dict_collection[index], []))

    return list(set(remove_first_dot_input_lst_of_lst(out)[0]))
