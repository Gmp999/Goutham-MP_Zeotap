class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" for AND/OR, "operand" for conditions
        self.left = left
        self.right = right
        self.value = value  # e.g., a comparison like age > 30

import ast

# Helper function to map comparison operators
OPERATORS = {
    ast.And: "AND",
    ast.Or: "OR",
    ast.Gt: ">",
    ast.Lt: "<",
    ast.Eq: "=="
}

def create_rule(rule_string):
    # Convert AND/OR to lowercase for consistent processing
    rule_string = rule_string.replace("AND", "and").replace("OR", "or")

    # Replace '=' with '==' for valid Python syntax
    rule_string = rule_string.replace("=", "==")

    # Parse the modified rule string
    parsed = ast.parse(rule_string, mode='eval')

    def build_ast(node):
        if isinstance(node, ast.BoolOp):  # AND / OR
            op_type = OPERATORS[type(node.op)]
            left_node = build_ast(node.values[0])
            right_node = build_ast(node.values[1])
            return Node(node_type="operator", left=left_node, right=right_node, value=op_type)
        elif isinstance(node, ast.Compare):  # Operand
            left = node.left.id
            op = OPERATORS[type(node.ops[0])]
            right = node.comparators[0].n
            return Node(node_type="operand", value=f"{left} {op} {right}")
        else:
            raise ValueError("Unsupported expression")

    return build_ast(parsed.body)

def combine_rules(rules, combine_op="AND"):
    if not rules:
        return None

    current_ast = rules[0]
    for next_rule in rules[1:]:
        combined_ast = Node(node_type="operator", left=current_ast, right=next_rule, value=combine_op)
        current_ast = combined_ast

    return current_ast

def evaluate_rule(ast_node, data):
    if ast_node.type == "operand":
        # Evaluate the operand condition
        left, op, right = ast_node.value.split()
        left_value = data.get(left)

        # Convert to appropriate types
        right_value = int(right) if right.isdigit() else right.strip("'")

        # Perform the comparison
        if op == ">":
            return left_value > right_value
        elif op == "<":
            return left_value < right_value
        elif op == "==":  # Check for equality operator
            return left_value == right_value
        else:
            raise ValueError("Unsupported operator")

    elif ast_node.type == "operator":
        # Evaluate left and right child nodes
        left_result = evaluate_rule(ast_node.left, data)
        right_result = evaluate_rule(ast_node.right, data)

        # Perform the AND/OR operation
        if ast_node.value == "AND":
            return left_result and right_result
        elif ast_node.value == "OR":
            return left_result or right_result
        else:
            raise ValueError("Unsupported logical operator")

    else:
        raise ValueError("Unsupported node type")

# Example usage
rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
ast_rule1 = create_rule(rule1)

# Example usage
rule2 = "age < 25 AND department = 'Marketing'"
ast_rule2 = create_rule(rule2)
combined_ast = combine_rules([ast_rule1, ast_rule2], combine_op="OR")

# Example data for evaluation
sample_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 6}
result = evaluate_rule(combined_ast, sample_data)
print("Eligibility:", result)
