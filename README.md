

import ast

with open('tên_file_spider.py', 'r') as file:
    content = file.read()

# Phân tích cú pháp file Python
tree = ast.parse(content)

# Tìm và lấy giá trị của thuộc tính 'name'
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        for class_node in node.body:
            if (
                isinstance(class_node, ast.Assign)
                and len(class_node.targets) == 1
                and isinstance(class_node.targets[0], ast.Name)
                and class_node.targets[0].id == 'name'
            ):
                spider_name = class_node.value.s
                print(f"Thuộc tính 'name' của spider là: {spider_name}")
