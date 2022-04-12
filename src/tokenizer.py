import re
import xml.etree.ElementPath as ElementPath

def short_syntax_xpath_tokenizer(p):
    """
    Test the XPath tokenizer.

    >>> # tests from the xml specification
    >>> xpath_tokenizer("*")
    ['*']
    >>> xpath_tokenizer("text()")
    ['text', '()']
    >>> xpath_tokenizer("@name")
    ['@', 'name']
    >>> xpath_tokenizer("@*")
    ['@', '*']
    >>> xpath_tokenizer("para[1]")
    ['para', '[', '1', ']']
    >>> xpath_tokenizer("para[last()]")
    ['para', '[', 'last', '()', ']']
    >>> xpath_tokenizer("*/para")
    ['*', '/', 'para']
    >>> xpath_tokenizer("/doc/chapter[5]/section[2]")
    ['/', 'doc', '/', 'chapter', '[', '5', ']', '/', 'section', '[', '2', ']']
    >>> xpath_tokenizer("chapter//para")
    ['chapter', '//', 'para']
    >>> xpath_tokenizer("//para")
    ['//', 'para']
    >>> xpath_tokenizer("//olist/item")
    ['//', 'olist', '/', 'item']
    >>> xpath_tokenizer(".")
    ['.']
    >>> xpath_tokenizer(".//para")
    ['.', '//', 'para']
    >>> xpath_tokenizer("..")
    ['..']
    >>> xpath_tokenizer("../@lang")
    ['..', '/', '@', 'lang']
    >>> xpath_tokenizer("chapter[title]")
    ['chapter', '[', 'title', ']']
    >>> xpath_tokenizer("employee[@secretary and @assistant]")
    ['employee', '[', '@', 'secretary', '', 'and', '', '@', 'assistant', ']']

    >>> # additional tests
    >>> xpath_tokenizer("{http://spam}egg")
    ['{http://spam}egg']
    >>> xpath_tokenizer("./spam.egg")
    ['.', '/', 'spam.egg']
    >>> xpath_tokenizer(".//{http://spam}egg")
    ['.', '//', '{http://spam}egg']
    """
    out = []
    for op, tag in ElementPath.xpath_tokenizer(p):
        out.append(op or tag)
    return out


def full_syntax_xpath_tokenizer(expression):
    '''
    Test the XPath tokenizer for full syntax
    
    >>> full_syntax_xpath_tokenizer("/child::a/child::b")
    ['/', 'child::a', '/', 'child::b']
    >>> full_syntax_xpath_tokenizer("/descendant::b/child::c")
    ['/', 'descendant::b', '/', 'child::c']
    >>> full_syntax_xpath_tokenizer("/child::a[child::b < 5]")
    ['/', 'child::a', '[', 'child::b', '<', '5', ']']
    >>> full_syntax_xpath_tokenizer("/child::a[attribute::b < 5]")
    ['/', 'child::a', '[', 'attribute::b', '<', '5', ']']
    >>> full_syntax_xpath_tokenizer("/child::a[child::b < 5 and child::c > 6]")
    ['/', 'child::a', '[', 'child::b', '<', '5', 'and', 'child::c', '>', '6', ']']
    >>> full_syntax_xpath_tokenizer("/child::a[child::b = ’A’]")
    ['/', 'child::a', '[', 'child::b', '=', '’A’', ']']
    >>> full_syntax_xpath_tokenizer("/child::a/*")
    ['/', 'child::a', '/', '*']
    >>> full_syntax_xpath_tokenizer("/child::d | /child::e")
    ['/', 'child::d', '|', '/', 'child::e']
    >>> full_syntax_xpath_tokenizer("/child::a/text()")
    ['/', 'child::a', '/', 'text', '()']
    '''

    xpath_tokenizer_re = re.compile(
    r"("
    r"'[^']*'|\"[^\"]*\"|"
    r"::|"
    r"//?|"
    r"\.\.|"
    r"\(\)|"
    r"[/.*:\[\]\(\)@=])|"
    r"((?:\{[^}]+\})?[^/\[\]\(\)@=\s]+)|"
    r"\s+"
    )
    
    out = []
    for token in xpath_tokenizer_re.findall(expression):
        for t in token:
            if t != '':
                out.append(t)
    return out

def tokenize(xPath: str):
    path = ''
    if "::" in xPath:
        full_syntax_xpath_tokenizer_list = full_syntax_xpath_tokenizer(xPath)

        for f in full_syntax_xpath_tokenizer_list:
            if 'child::' in f:
                f = f.replace('child::', '')
            if 'descendant::' in f:
                f = f.replace('descendant::', '/')
            if (f == 'and') or (f == 'or') or (f == '(') or (f == ')'):
                f = " " + f + " "
            path += f
    else:
        path = xPath

    return short_syntax_xpath_tokenizer(path)
