# XMongo

Design and implementation of a compiler for an XPath dialect for JSON and MongoDB.

# About

This library provides allow you to input a XPath and it will output the corresponding MongoDB query that will obtain the same output result.

# Quick Start

- To install, use pip:
- If you are using python version 3, then it will be `pip3` and `python3`

```bash
pip install pymongo certifi
```

# Usage on local machine

You can choose to run the sample library.json or bookstore.json which can be found in `src/sample`. You can choose either to run the sample queries or input your own queries.

```bash
python main.py
```

# Usage with MongoDB Atlas

- Set up your own [MongoDB Cloud Altas Database](https://www.mongodb.com/cloud/atlas/register1)
- Create your own database and collections
- Connect your sandbox using the python driver
- Replace the `cluster` in `mainAtlas.py` and the `XXX` with your own `USERNAME` and `PASSWORD`
- Replace `DATABASE` and `COLLECTION` with the respective database and collection name in cloud respectively

```bash
python mainAtlas.py
```

# Support

The XPath syntax supported by this library are features are child, descendants, predicates, conditions, attributes. It is also able to support full path and short path syntax. However, it omits some problematic features such as `|`, `sibling`, `ancestor` and `parent`.

The following type of queries are supported:

1. only_child_axes
2. only_descendant_axes
3. both_child_descendant_axes
4. only_child_axes_with_star
5. only_descendant_axes_with_star
6. only_child_axes_with_single_condition
7. only_child_axes_with_multiple_condition
8. only_child_axes_with_predicates_condition
9. only_child_axes_with_nested_condition
