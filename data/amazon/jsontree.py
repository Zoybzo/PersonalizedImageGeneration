"""
将json数据转换为tree
"""

from treelib import Tree, Node


tree = Tree()
tree.create_node("Item", "Item")


def add_nodes(parent_id, parent_data):
    for key, value in parent_data.items():
        node_name = key
        if parent_id != node_name:
            tree.create_node(node_name, node_name, parent=parent_id)
        node_sons = value
    for values in node_sons.values():
        for att in values:
            if isinstance(att, str):
                tree.create_node(att, att, parent=node_name)
            else:
                add_nodes(node_name, att)


def get_tree(json_data):
    """
    从json数据中获取tree

    Args:
        json_data: dict, json数据
    """
    add_nodes("Item", json_data)
    return tree
