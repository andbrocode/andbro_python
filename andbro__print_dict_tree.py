def print_dict_tree(d, indent=0, prefix=""):
    """
    Print a dictionary's keys in a tree-like structure.
    
    Args:
        d (dict): The dictionary to display
        indent (int): Current indentation level
        prefix (str): Prefix for the current line
    """
    for i, (key, value) in enumerate(d.items()):
        is_last = i == len(d) - 1
        current_prefix = "└── " if is_last else "├── "
        print(" " * indent + prefix + current_prefix + str(key))
        
        if isinstance(value, dict):
            next_prefix = "    " if is_last else "│   "
            print_dict_tree(value, indent + 4, prefix + next_prefix)
