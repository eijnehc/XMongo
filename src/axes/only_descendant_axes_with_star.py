from src.tokenizer import tokenize

def only_descendant_axes_with_star(xPath, schema):
    token_list = tokenize(xPath)

    sliced_list_without_slash = list(filter(lambda a: a != '//', token_list))
    projection = {}

    for token in sliced_list_without_slash:
        for s in schema:
            if token in s:
                projection[s] =1

    return {}, projection