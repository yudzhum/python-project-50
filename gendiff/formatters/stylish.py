from itertools import chain


VALUES_TO_CONVERT = [True, False, None]
ADDED = '  + '
REMOVED = '  - '
UNCHANGED = '    '
UPDATED = '  - '


def get_value(node):
    """Get value of node"""

    return node.get('value')


def get_changed_value(node):
    """Get changed_value of node"""

    return node.get('changed_value')


def get_name(node):
    """Get name of node"""

    return node.get('name')


def get_status(node):
    """Get status mark based of node type"""

    type = node.get('type')
    status = UNCHANGED
    if type == 'added':
        status = ADDED
    elif type == 'removed':
        status = REMOVED
    elif type == 'unchanged':
        status = UNCHANGED
    elif type == 'updated':
        if is_leaf(node):
            status = UPDATED
    return status


def get_type(node):
    """Get type of node"""

    return node.get('type')


def get_children(node):
    """
    Return children(list) from node.
    If object is list return list
    """
    if isinstance(node, list):
        return node
    return node.get('children')


def is_leaf(node):
    """
    Return true if object is node(dict)
    without children
    """
    if isinstance(node, list):
        return False
    if get_children(node):
        return False
    return True


def convert(value):
    """
    Convert values:
    False -> false, True -> true, None -> null
    """
    if value is None:
        return 'null'
    return str(value).lower()


def stringify(value, depth, replacer=' ', spaces_count=1,):
    """Take value and return string"""

    def iter_(current_value, depth):
        # Primitive value case
        if not isinstance(current_value, dict):
            # If current value False, True, None
            # convert to false, true, null
            if current_value in VALUES_TO_CONVERT:
                return convert(value)
            return str(current_value)

        # Calculate intend
        deep_indent_size = depth + spaces_count
        deep_indent = replacer * deep_indent_size
        current_indent = replacer * depth

        # Value is a dictionary
        lines = []
        for key, val in current_value.items():
            lines.append(f'{deep_indent}{key}: {iter_(val, deep_indent_size)}')
        result = chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(value, depth)


def handler_(node, depth, replacer):
    """Take dict(node without children), return value as formatted string"""

    value = stringify(get_value(node), depth, replacer)

    if get_type(node) == 'updated':
        changed_value = stringify(get_changed_value(node), depth, replacer)
        intend = replacer * (depth - 1)
        return (f'{value}'
                f'\n{intend}{ADDED}{get_name(node)}: {changed_value}')

    return value


def stylish(tree, replacer='    ', spaces_count=1):
    """
    Take diff tree, walks the tree recursively,
    and return data as formatted string.
    """

    def iter_(node, depth):
        # Node has no children
        if is_leaf(node):
            value = handler_(node, depth, replacer)
            return value

        # Calculate intend
        deep_indent_size = depth + spaces_count
        current_indent = replacer * depth

        # Node has children
        children = get_children(node)

        lines = []
        for child in children:
            status = get_status(child)
            # Append string look like '(intend)key: styled_value'
            lines.append(
                f'{current_indent}{status}{get_name(child)}: '
                f'{iter_(child, deep_indent_size)}'
            )

        result = chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(tree, 0)
