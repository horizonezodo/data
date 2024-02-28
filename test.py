import ast


def extract_xpath_from_parse_function(file_path):
    with open(file_path,'r') as file:
        script_content = file.read()
        tree = ast.parse(script_content)

        csspaths = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and hasattr(node.func, 'attr') and node.func.attr == 'css':
                csspath = node.args[0].s
                csspaths.append(csspath)

        return csspaths

def extract_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    parsed_content = ast.parse(content)
    for node in ast.walk(parsed_content):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == 'name':
                        name = ast.literal_eval(node.value)
                    elif target.id == 'allowed_domains':
                        allowed_domains = ast.literal_eval(node.value)
                    elif target.id == 'start_urls':
                        start_urls = ast.literal_eval(node.value)
    return name,allowed_domains,start_urls

def get_url_value_data(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        tree = ast.parse(content)

        # Tìm và lấy giá trị của biến url_value
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Name) and target.id == "url_value":
                    url_value_node = node.value
                    url_value = ast.get_source_segment(content, url_value_node).strip()
                    break
    return url_value


name, allowed_domains,start_url = extract_data('E:\\testProject\\testProject\\spiders\\123nhadatviet.py')
url_css = get_url_value_data('E:\\testProject\\testProject\\spiders\\123nhadatviet.py')
csspaths = extract_xpath_from_parse_function('E:\\testProject\\testProject\\spiders\\123nhadatviet.py')
question_css = csspaths[0]
title_css = csspaths[1]
detail_css = csspaths[2]
price_css = csspaths[3]
square_css = csspaths[4]


print('url_css: ' + url_css)
print('name: '+name)
print('domain')
print(allowed_domains)
print('start_url')
print(start_url)
print('question_css: '+question_css)
print('title_css: '+title_css)
print('detail_css: '+detail_css)
print('price_css: '+price_css)
print('square_css: '+square_css)







