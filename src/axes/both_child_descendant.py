from src.tokenizer import tokenize

def remove_rootElement_documentName_if_exists(tokens, schema):
    out = []

    for index, xpath_value in enumerate(tokens): 
        is_xpath_value_a_rootElement_documentName = False 
        for path in schema:     
            if xpath_value in path.split("."):        
                is_xpath_value_a_rootElement_documentName = True
                break
    
        if is_xpath_value_a_rootElement_documentName == True:
            #line below is to append the / or // before the word
            out.append(tokens[index-1])
            
            #line below is to append the  word
            out.append(xpath_value)  
    
    return out

def construct_db_syntax_both_child_descendant(xpath_tokens_list, all_key_paths_list_first_doc_remove_duplicates):  
    out_list = []
    found_paths_list_raw = []
    found_paths_list = []
    unique_i_tokens = []
    
    # you need to keep track of the symbol if it is / or // in front of the word   
    for i in xpath_tokens_list:    
        if i == '/':
            previous = '/'
        elif i == '//':
            previous = '//'
        else: 
            if previous == '/':
                unique_i_tokens.append(i)
                # Iterate for every path and check if the word i is in the path
                # For eg, //title appears in 'title' and 'songs.song.title'
                for path in all_key_paths_list_first_doc_remove_duplicates:
                    if i in path:
                        found_paths_list_raw.append(path)                
            
            if previous == '//':
                unique_i_tokens.append(i)
                # Iterate for every path and check if the word i is in the path
                # For eg, //title appears in 'title' and 'songs.song.title'
                for path in all_key_paths_list_first_doc_remove_duplicates:
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

def both_child_descendant(xPath, schema):
    #Step 1: Input full syntax xpath expression -> Output list of xpath short syntax tokens 
    tokens = tokenize(xPath)
    
    # So now we write a custom function to remove root element and document name if any
    no_root_elements_tokens = remove_rootElement_documentName_if_exists(tokens, schema)

    #Step3: Now we have to do the construction of db syntax
    xpath_construct_db_list = construct_db_syntax_both_child_descendant (no_root_elements_tokens, schema)
    
    projection = dict()
    
    for str_x_value in xpath_construct_db_list:
        projection[str_x_value] = 1

    return {}, projection