class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # Reference to another Node (left child)
        self.right = right     # Reference to another Node (right child for operators)
        self.value = value     # Optional value for operand nodes

def create_rule(rule_string):
    # Simplified parser; this should be more complex for full AST generation
    # You can implement a proper parser to generate an AST based on your rules.
    # Here is a placeholder implementation.
    if 'AND' in rule_string:
        left, right = rule_string.split(' AND ')
        return Node('operator', create_rule(left), create_rule(right))
    elif 'OR' in rule_string:
        left, right = rule_string.split(' OR ')
        return Node('operator', create_rule(left), create_rule(right))
    else:
        # Extracting condition as a leaf node
        return Node('operand', value=rule_string.strip())


def combine_rules(rules):
    combined = Node('operator')  # Root node of the combined AST
    for rule in rules:
        combined.right = create_rule(rule)
    return combined

def evaluate_rule(ast, data):
    if ast.type == 'operand':
        # Evaluate the condition; This will need to be a proper evaluation logic
        # Here we assume a simple eval just for demonstration.
        return eval(ast.value.format(**data))
    elif ast.type == 'operator':
        left_result = evaluate_rule(ast.left, data) if ast.left else True
        right_result = evaluate_rule(ast.right, data) if ast.right else True

        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result

    return False
