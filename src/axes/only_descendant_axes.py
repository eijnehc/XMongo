from src.tokenizer import tokenize

def construct_db_syntax_only_descendant_axes (xpath_tokens_list, schema):
    out_list = []
    found_paths_list_raw = []
    found_paths_list = []
    unique_i_tokens = []
    
    #Step1: Iterate for each descendant token, eg //First_Name//Title.. so there are 2 tokens
    for i in xpath_tokens_list:
        #this logic here is not so simple as the child axes, you need to reconstruct the parent, ancestors. 
        #For eg, //First_Name => need to reconstruct to Authors.Author.First_Name
        if i != '//':
            unique_i_tokens.append(i)

            # Iterate for every path and check if the word i is in the path
            # For eg, //title appears in 'title' and 'songs.song.title'
            for path in schema:                
                if i in path:
                        found_paths_list_raw.append(path)

    # Step2: Step1 consists of incorrect found_paths_list, because when i initally traverse, i do not know the later part of the xpath tokens
    for f_p in found_paths_list_raw:
        if set(unique_i_tokens).issubset(f_p.split(".")) and (f_p not in found_paths_list):
            found_paths_list.append(f_p)

    # Step3:We want to append the found_path_elements one by one until it reaches the i token
    for f_p in found_paths_list:
        out_inner_list = []
        f_p_list = f_p.split(".")
        
        for f_p_element in f_p_list:
            if (f_p_element != i) and (f_p_element not in out_inner_list):
                out_inner_list.append(f_p_element)
            elif (f_p_element == i):
                break
        
        out_inner_list.append(f_p_element)
        
        if out_inner_list not in out_list:     
            out_list.append(out_inner_list)
    
    out_string_list = []
    for o in out_list:
        if type(o) == list:
            out_string = ''
            for index, o_value in enumerate(o):
                if index != (len(o) - 1):
                    out_string = out_string + o_value + '.'
                else:
                    out_string = out_string + o_value

        out_string_list.append(out_string)
        
    return out_string_list

def only_descendant_axes(xPath, schema):
    #Step 1: Input full syntax xpath expression -> Output list of xpath short syntax tokens 
    tokens = tokenize(xPath)

    #Step2: We slice the list of xpath short syntax tokens
    # Since this is Case2: only_descendant_axes, the elements are ['//', 'Sth', '//', ...]
    # I am just removing the 1st '//'
    slice_short_syntax_xpath_tokenizer_list = tokens[1:]
    
    #Step3: We construct the MongoDB syntax from the remaining xpath tokens
    xpath_construct_db_list = construct_db_syntax_only_descendant_axes(slice_short_syntax_xpath_tokenizer_list, schema)
    
    projection = dict()
    
    for str_x_value in xpath_construct_db_list:
        projection[str_x_value] = 1

    return { }, projection

    
