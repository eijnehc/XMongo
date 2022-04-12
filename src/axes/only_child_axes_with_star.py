from src.tokenizer import tokenize

def only_child_axes_with_star(xPath, schema):
    tokens_list = tokenize(xPath)
    
    sliced_list = tokens_list[5:]
        
    sliced_list_without_slash = list(filter(lambda a: a != '/', sliced_list))
    
    is_all_star = True

    for token in sliced_list_without_slash:
        if token != "*":
            is_all_star = False

    if (is_all_star):
        return {}, {}
        
    else:        
        projection = {}
        depth = len(sliced_list_without_slash)

        for token in sliced_list_without_slash:
            for s in schema:
                s_length = len(s.split("."))
                if token in s and s_length >= depth:
                    projection[s] = 1

        return {}, projection
