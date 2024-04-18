import json

from treelib import Tree, Node

from data.amazon.JsonTree import get_tree

CATEGORY = [
    "Clothing",
    "Shoes",
    "Jewelry",
    "Watch",
    "Makeup",
    "Appliances",
    "Car",
    "Books",
    "Electronics",
    "Food",
    "Movie",
    "Office_Product",
    "Sport",
    "Toy",
    "Game",
    "Restaurant",
    "Bar",
    "Hotel",
]
EXTRA_PRODUCT = [
    "Pants",
    "T-shirts",
    "Coat",
    "Dress",
    "Phone",
    "Computer",
    "Earphone",
    "BaskerBall",
    "Racket",
]


def creat_attribute_node(parent_name, tag_name, attribute_list):
    assert isinstance(attribute_list, list), "请输入属性List"
    new_tree = Tree()
    new_tree.create_node(tag_name, tag_name)
    for attr in attribute_list:
        new_tree.create_node(attr, attr, parent=tag_name)

    # tree.paste(parent_name, new_tree)
    return parent_name, new_tree


def add_subtree(parent_name, tag_name, tree, sub_tree):
    if tree.contains(tag_name):
        tree.remove_node(tag_name)
    tree.paste(parent_name, sub_tree)

    return tree


def init_category_tree(category):
    tree = Tree()
    tree.create_node("Item", "Item")
    for categ in category:
        tree.create_node(categ, categ, parent="Item")
    return tree


def save_tree_to_json(file_name, tree):
    assert isinstance(tree, Tree), "请输入treelib的Tree"
    json_data = tree.to_json(with_data=False)
    tree_data = json.loads(json_data)
    with open(file_name, "w") as f:
        json.dump(tree_data, f)


def load_json_to_tree(json_file):
    """
    从json文件中加载tree
    """
    with open(json_file, "r") as f:
        json_data = json.load(f)
    tree = get_tree(json_data)
    return tree


def add_node_updata_tree(json_path, attribute_list, parent_name, tag_name):
    tree = load_json_to_tree(json_path)
    parent_name, std_tree = creat_attribute_node(parent_name, tag_name, attribute_list)
    tree = add_subtree(parent_name, tag_name, tree, std_tree)
    save_tree_to_json(json_path, tree)
    return tree


if __name__ == "__main__":
    print("test")
    # tree = init_category_tree(CATEGORY)
    # print(tree.to_json(with_data=False))
    json_path = "J:/zym/Item_Agent/Planning_Tree/item_tree.json"
    tree = load_json_to_tree(json_path)
    # print(tree.to_json(with_data=False))
    # # # print(tree.to_json(with_data=False))
    attribute_list = ["image_text", "beauty_color", "beauty_type"]
    parent_name = "Item"
    tag_name = "Beauty"
    parent_name, std_tree = creat_attribute_node(parent_name, tag_name, attribute_list)
    # print(std_tree.to_json(with_data=False))
    tree = add_subtree(parent_name, tag_name, tree, std_tree)
    print(tree.to_json(with_data=False))
    save_tree_to_json(json_path, tree)
    for node in tree.children("Beauty"):
        print(node.tag)
    # json_path = "J:/zym/Item_Agent/Planning_Tree/item_tree.json"
    # tree = load_json_to_tree(json_path)
    # print(tree.to_json(with_data=False))
