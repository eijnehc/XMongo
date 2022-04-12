from src.axes.both_child_descendant import both_child_descendant
from src.axes.only_child_axes_with_condition import only_child_axes_with_condition
from src.axes.only_child_axes import only_child_axes
from src.axes.only_descendant_axes import only_descendant_axes
from src.axes.only_child_axes_with_star import only_child_axes_with_star
from src.axes.only_descendant_axes_with_star import only_descendant_axes_with_star
from src.tokenizer import tokenize 

def xPath_classifier(xpath_tokenizer_lst):
    '''
    Symbols Identifier
    symbol_1: /
    symbol_2: [
    symbol_3: ]
    symbol_4: | 
    symbol_5: >
    symbol_6: <
    symbol_7: =
    symbol_8: *
    
    Words Identifier
    word_1: child::
    word_2: descendant::
    word_3: attribute::
    word_4: and
    word_5: or
    word_6: count
    word_7 = 'sum'
    others: anything that i haven thought of
    '''
    symbol_1 = '/'
    symbol_2 = '['
    symbol_3 = ']'
    symbol_4 = '|' 
    symbol_5 = '>'
    symbol_6 = '<'
    symbol_7 = '='
    symbol_8 = '*'
    symbol_9 = '//'
    
    symbol_1_count = 0 
    symbol_2_count = 0 
    symbol_3_count = 0 
    symbol_4_count = 0 
    symbol_5_count = 0 
    symbol_6_count = 0 
    symbol_7_count = 0 
    symbol_8_count = 0 
    symbol_9_count = 0

    for x in xpath_tokenizer_lst:
        if x == symbol_1:
            symbol_1_count += 1
        if x == symbol_2:
            symbol_2_count += 1
        if x == symbol_3:
            symbol_3_count += 1
        if x == symbol_4:
            symbol_4_count += 1
        if x == symbol_5:
            symbol_5_count += 1
        if x == symbol_6:
            symbol_6_count += 1
        if x == symbol_7:
            symbol_7_count += 1
        if x == symbol_8:
            symbol_8_count += 1
        if x == symbol_9:
            symbol_9_count += 1  

    if (symbol_1_count > 0) and (symbol_2_count == 0) and (symbol_4_count == 0) and (symbol_5_count == 0) and (symbol_6_count == 0) and (symbol_7_count == 0) and (symbol_8_count == 0) and (symbol_9_count == 0):
        return "only_child_axes"
    if (symbol_1_count == 0) and (symbol_9_count > 0) and  (symbol_2_count == 0) and (symbol_4_count == 0) and (symbol_5_count == 0) and (symbol_6_count == 0) and (symbol_7_count == 0) and (symbol_8_count == 0):
        return "only_descendant_axes"
    if (symbol_1_count > 0) and (symbol_9_count > 0) and (symbol_2_count == 0) and (symbol_4_count == 0) and (symbol_5_count == 0) and (symbol_6_count == 0) and (symbol_7_count == 0) and (symbol_8_count == 0):
        return "both_child_descendant"
    if (symbol_1_count > 0) and (symbol_9_count == 0) and (symbol_2_count > 0) and (symbol_8_count == 0):
        return "only_child_axes_with_condition"
    if (symbol_1_count > 0) and (symbol_2_count == 0) and (symbol_8_count > 0) and (symbol_9_count == 0):
        return "only_child_axes_with_star"
    if (symbol_1_count == 0) and (symbol_2_count == 0) and (symbol_8_count > 0) and (symbol_9_count > 0):
        return "only_descendant_axes_with_star"
    
    return "Invalid Query"

VALID_SPECIAL_CHARACTER = ['/', '//', '[', ']', '*', '@', '<', '>', '>=', '<=', '=']

def checkValidXPath(xPath, schema):
    tokens = tokenize(xPath)

    if '/' not in xPath:
        return False
    tokens_strip_empty = list(filter(lambda a: a != '', tokens))
    
    for token in tokens_strip_empty:
        isValid = False
        for s in schema:
            if token in s.split('.') or token in VALID_SPECIAL_CHARACTER or token[0] == '\'' :
                isValid = True
        
    if not isValid:
        return False

    return True
    

def mongo_query(xPath, schema):
    isValidXPath = checkValidXPath(xPath, schema)
    
    xPath_class = xPath_classifier(tokenize(xPath))

    if isValidXPath:
        if xPath_class == "only_child_axes":
            return only_child_axes(xPath, schema)
        if xPath_class == "only_descendant_axes":
            return only_descendant_axes(xPath, schema)
        if xPath_class == "both_child_descendant":
            return both_child_descendant(xPath, schema)
        if xPath_class == "only_child_axes_with_condition":
            return only_child_axes_with_condition(xPath, schema)
        if xPath_class == "only_child_axes_with_star":
            return only_child_axes_with_star(xPath, schema)
        if xPath_class == "only_descendant_axes_with_star":
            return only_descendant_axes_with_star(xPath, schema)
        if xPath_class == 'Invalid Query':
            return "Invalid Syntax"
    else:
        return 'Invalid Syntax', 'Invalid Syntax'
    





