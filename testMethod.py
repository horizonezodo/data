import ast
import os
import re
import shutil
import subprocess
import sys


def get_website_detail(file_path):
    with open(file_path, 'r') as file:
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
                    return spider_name


def run_commands(json_file_path):
    # Thay đổi thư mục làm việc
    subprocess.run(["cd", "/d", "E:\\python_leaning\\TestPython\\crawler\\venv"], shell=True)

    # Kích hoạt môi trường ảo
    subprocess.run(["E:\\python_leaning\\TestPython\\crawler\\venv\\Scripts\\activate"], shell=True)

    # Thay đổi thư mục làm việc
    subprocess.run(["cd", "E:\\python_leaning\\TestPython\\crawler\\crawler\\spiders\\"], shell=True)

    # Chạy tệp python với đường dẫn JSON được truyền vào từ dòng lệnh
    subprocess.run(["python", "E:\\python_leaning\\TestPython\\crawler\\crawler\\spiders\\run_scrawler.py", json_file_path], shell=True)

if __name__ == "__main__":
    # Lấy đường dẫn tệp JSON từ dòng lệnh
    #json_file_path = sys.argv[1]
    source_file = 'E:\\testProject\\testProject\\spiders\\123nhadatviet.py'

    # Đường dẫn của thư mục đích
    destination_directory = 'E:\\python_leaning\\TestPython\\crawler\\crawler\\spiders\\'

    # Thực hiện copy file từ nguồn sang đích
    shutil.copy2(source_file, destination_directory)

    # Kiểm tra xem file đích đã tồn tại hay chưa
    destination_file = os.path.join(destination_directory, os.path.basename(source_file))
    name = get_website_detail(destination_file)
    print(name)

    run_commands(destination_file)

    # if os.path.exists(destination_file):
    #     # Xóa file copy
    #     os.remove(destination_file)
    #     print(f"Đã xóa file copy: {destination_file}")
    # else:
    #     print("File copy không tồn tại.")
