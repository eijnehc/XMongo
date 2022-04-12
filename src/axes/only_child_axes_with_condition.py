from src.tokenizer import tokenize, full_syntax_xpath_tokenizer
from src.axes.only_child_axes import only_child_axes
from string import ascii_lowercase

OPERANDS = ["=", ">", "<", ">=", "<="]
PREDICATES = ['and', 'or', '(', ')']

def flatten_list(string, recursion_counter = 0, output_list = []):    
    #Initial conditions:
    count_left_bracket_condition = 0
    count_right_bracket_condition = 0
    left_sub_str = ''

    #traverse the string
    for index, s_value in enumerate(string):
        if s_value == "[":
            count_left_bracket_condition += 1
            break 
        if s_value == "]":
            count_right_bracket_condition += 1
            break
        if count_left_bracket_condition > 0 or count_right_bracket_condition > 0: 
            break
        
        left_sub_str = left_sub_str + s_value
    
    if left_sub_str not in output_list and left_sub_str != '':
        output_list.append(left_sub_str)
    
    #Base case if there is no [ then return string
    if count_left_bracket_condition == count_right_bracket_condition:
        
        return output_list
    
    # Case1 where there is left bracket but no right bracket
    if count_left_bracket_condition > count_right_bracket_condition:
        sub_str_after_left_bracket = string[index+1:]
        
        # pass the remaining sub_str_after_left_bracket into the function 
        # sub_str_after_left_recur_res = recursion_test (sub_str_after_left_bracket)

        # Note what is the difference between the 2 lines of return?
        # Observe that if the list contains a /sth, that sth is the last node to query        
        return flatten_list( "/" + sub_str_after_left_bracket, recursion_counter+1, output_list)
    
    # Case2 where there is right bracket but no left bracket
    if count_right_bracket_condition > count_left_bracket_condition:
        sub_str_after_right_bracket = string[index+1:]
        
        # pass the remaining sub_str_after_right_bracket into the function 
        # sub_str_after_right_recur_res = recursion_test (sub_str_after_right_bracket)
        return flatten_list(sub_str_after_right_bracket, recursion_counter+1, output_list) 

def projection_filter_substr(xpath):
    flatten_list_result = flatten_list(xpath, recursion_counter = 0, output_list = [])

    projection_path = ''
    filter_path_list = []

    # Add in all the filter conditions
    for i in flatten_list_result:
        if ("=" in i) or (">" in i) or ("<" in i) or (">=" in i) or ("<=" in i):
            filter_path_list.append(i)
    
    # Try to form the projection path
    for i in flatten_list_result:
        if i[0] == "/" and not (("=" in i) or (">" in i) or ("<" in i) or (">=" in i) or ("<=" in i)):
            projection_path += i
    
    return filter_path_list, projection_path

def split_predicates(filter_path):
    tokens = tokenize(filter_path)

    result = []
    s = ''

    for token in tokens:
        if (token != 'and') and (token != 'or') and (token != '(') and (token != ')'):
            s += token
        
        else:
            if s != '':
                result.append(s)
            
            if token != '':
                result.append(token)
            
            s = ''
    #append one last time
    if s != '':
        result.append(s)

    return result

def filter_architecture(filter_path_list):
    filter_list = []

    for filter_path in filter_path_list:
        # you want a list and not nested list [[],[]]
        filter_list.extend(split_predicates(filter_path))

    # this for loop to get ["/child::title='No War'", 'child::year=1997', 'child::year=1996']
    children_without_predicate = []
    for token in filter_list:
        if token not in PREDICATES and token != "":
            children_without_predicate.append(token)
    
    # this for loop to get ['a', 'and', '(', 'b', 'or', 'c', ')'])
    children_count = 0
    for index, token in enumerate(filter_list):
        if token not in PREDICATES:
            filter_list[index] = ascii_lowercase[children_count]
            children_count += 1

    filter_syntax = ''
    for c in filter_list:
        filter_syntax = filter_syntax + c + ' '
    
    return children_without_predicate, filter_syntax

def custom_splitter_by_outer_operator(op_string):
    op_string_list1 = full_syntax_xpath_tokenizer (op_string)
    
    op_string_list2 = []
    formstring = ''
    counter_open_parathesis = 0 # if value > 0, it means the traversal is after ( but before )

    for op in op_string_list1:
        if op == "(":
            counter_open_parathesis += 1
        
        if op == ")":
            counter_open_parathesis -= 1
        
        if counter_open_parathesis > 0:
            formstring = formstring + op + ' '
        
        if counter_open_parathesis == 0 and formstring == '':
            op_string_list2.append(op)
        
        if counter_open_parathesis == 0 and formstring != '':
            formstring = formstring + ")" + ' '
            op_string_list2.append(formstring)
            
            #reset formstring
            formstring = ''
    
    op_string_list2 = [x.strip() for x in op_string_list2]
    
    return op_string_list2

def recursion_op_test(raw_filter_syntax, condition_list):
    # I need to implement a logic here that transform op_string 
    # "/child::title = 'No War' and (child::year = 1997 or child::year = 1996)"
    # "        a                and (       b           or        c          )"

    cus_split_outer_op_list = custom_splitter_by_outer_operator(raw_filter_syntax)
    cus_split_outer_op_list_without_outer_op = []
    outer_operator = []
    #traverse the custom_splitter_by_outer_operator_list
    for i in cus_split_outer_op_list:
        if (i != 'and') and (i != 'or'):
            cus_split_outer_op_list_without_outer_op.append(i)
        if (i == 'and') or (i == 'or'):
            outer_operator.append(i)
    
    distint_outer_operator = list(set(outer_operator))
    need_recursion = False
    
    for c in cus_split_outer_op_list_without_outer_op:
        # check if each item in ['a', '( b or c )'], does it contains "and" or "or"
        if ("and" in c) or ("or" in c):
            need_recursion = True
    # Base Case: "a and b and c" , "a or b or c"
    base_syntax = dict()
    base_syntax[f"${distint_outer_operator[0]}"] = []

    if need_recursion == False:
        # Will look something like this {'$or': [{'a': ''}, {'b': ''}]}
        for index, token in enumerate(cus_split_outer_op_list_without_outer_op):
            field = dict()
            field[token] = ''
            base_syntax[f"${distint_outer_operator[0]}"].append(condition_list[index])

    if need_recursion == True:
        # { $and: [ {a} , { $or: [ {b} , {c} ] } ] }
        for index, token in enumerate(cus_split_outer_op_list_without_outer_op):
            if ('and' not in token) and ('or' not in token):
                field = dict()
                field[token] = ''
                base_syntax[f"${distint_outer_operator[0]}"].append(condition_list[index])
            else:
                base_syntax[f"${distint_outer_operator[0]}"].append(recursion_op_test(token[1:-1], condition_list[1:]))
        
    return base_syntax

def split_operand(token):
    operand = ''
    token_with_attribute = token

    if "@" in token:
        token_with_attribute = token.replace('@', '')

    if "=" in token_with_attribute:
        operand = "$eq"
        key_value = token_with_attribute.split("=") 
    if ">" in token:
        operand = "$gt"
        key_value = token_with_attribute.split(">")
    if "<" in token:
        operand = "$lt"
        key_value = token_with_attribute.split("<")
    if ">=" in token:
        operand = "$gte"
        key_value = token_with_attribute.split(">=")
    if "<=" in token:
        operand = "$lte"
        key_value = token_with_attribute.split("<=")

    return key_value, operand

def get_field(key_path, operand, value):
    field = dict()
    if (value.isnumeric()):
        # Will get an empty query if '1997' is used instead of 1997
        field[key_path] = {operand: int(value)}
    else:
        # Remove triple quotes {'$eq': "'No War'"}
        value_strip = value.strip('\"\'')
        field[key_path] = {operand: value_strip}
    
    return field
    
def get_filter_list(children_without_predicate, schema):
    for index, token in enumerate(children_without_predicate):
        #this is hardcode to remove the 1st / symbol in the token
        if token[0] == "/":
            children_without_predicate[index] = token[1:]
        else:
            children_without_predicate[index] = token

    # Now our list should look like
    # ["title='No War'", 'year=1997', 'year=1996']
    # ["artists/artist/name ='Kris Dayanti'", 'year=1997', 'year=1996']
    
    result = []

    # Sort schema base on the the depth in the tree using their dot
    sortedSchema = sorted(schema, key = lambda x: x.count("."))

    for token in children_without_predicate:
        # Have to split the token - "country='Indonesia'" to key:country and value:Indonesia. 
        key_value, operand = split_operand(token)
        key, value= key_value

        # key of songs/song/title to songs.song.title
        key_with_dot = key.replace("/", '.')

        isDuplicate = False
        # Use the key_without_slash to find the key path in schema
        for key_path in sortedSchema:
            if key_with_dot in key_path and not isDuplicate:                
                field = get_field(key_path, operand, value)
                result.append(field)
                isDuplicate = True 

    # [{'title': {'$eq': "'No War'"}}, {'year': {'$eq': '1997'}}, {'year': {'$eq': '1996'}}]
    return result

def convert_list_to_dictionary(condition_list):
    d = dict()
    for field in condition_list:
        d.update(field)
    
    return d

def only_child_axes_with_condition(xPath, schema):
    filter_path_list, projection_path = projection_filter_substr(xPath)
    filter, projection = only_child_axes(projection_path, schema)

    if len(filter_path_list) != 0:
        # transform_to_abc_syntax_for_recursion == filter_architecture
        children_without_predicate, raw_filter_syntax = filter_architecture(filter_path_list)

        filter_list = get_filter_list(children_without_predicate, schema)

        if ("or" in raw_filter_syntax or "and" in raw_filter_syntax):
            # Get the correct syntax form. "a or b" => "{ $or: [ {a} , {b} ] }"
            filter = recursion_op_test(raw_filter_syntax, filter_list)
        else:
            filter = convert_list_to_dictionary(filter_list)

        return filter, projection
    else:
        return filter, projection