from src.tokenizer import tokenize

def remove_slash(xPath_tokens):
    out = ''
    for i in xPath_tokens:
        if i != '/':
            out = out + i
        else:
            out = out + "."
    return out

def only_child_axes(xPath, schema):
    #Step 1: Input full syntax xpath expression -> Output list of xpath short syntax tokens 
    tokens = tokenize(xPath)

    #Step2: We slice the list of xpath short syntax tokens
    # Root Element in XML => MongoDB Collection
    # The 1st node after Root Element => Document name in MongoDB
    # Since this is Case1: only_child_axes, the first 4 elements are ['/', 'RootElement', '/', '1stNodeAfterRootElement', '/', ...]
    sliced_list = tokens[5:]

    if len(sliced_list) == 0:
        return { }, { }

    #Step3: We construct the MongoDB syntax from the remaining xpath tokens
    base_syntax = remove_slash(sliced_list)
    
    #Step4: Check if the XPath we are querying is valid
    is_valid = False

    for p in schema:
        if base_syntax in p:
            is_valid = True
    
    # Step5: We now need to print the FULL query return the baseSyntax for it to be place in <db.find({}, baseSyntax: 1)>
    if is_valid == True:

        return { }, { base_syntax: 1}