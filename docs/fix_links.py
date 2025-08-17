import csv
import os
import re

def fix_links(mapping_file="name_mapping.csv"):
    """使用映射表修复所有HTML文件中的链接"""
    # 读取映射表
    name_map = {}
    with open(mapping_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过标题行
        for row in reader:
            if len(row) >= 2:
                name_map[row[0]] = row[1]
    
    print(f"已加载 {len(name_map)} 个实体映射")
    
    # 遍历所有HTML文件
    fixed_count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    changed = False
                    
                    # 替换所有链接
                    for original_name, actual_filename in name_map.items():
                        # 创建可能出现的链接模式
                        old_link1 = f'individuals/{original_name}.html'
                        old_link2 = f'individuals/{original_name}'
                        old_link3 = f'"{original_name}.html"'
                        
                        # 创建新链接
                        new_link = f'individuals/{actual_filename}'
                        
                        # 替换所有可能的格式
                        if old_link1 in content:
                            new_content = new_content.replace(old_link1, new_link)
                            changed = True
                        if old_link2 in content:
                            new_content = new_content.replace(old_link2, new_link)
                            changed = True
                        if old_link3 in content:
                            new_content = new_content.replace(old_link3, f'"{new_link}"')
                            changed = True
                    
                    # 保存修改
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"已更新: {filepath}")
                        fixed_count += 1
                
                except Exception as e:
                    print(f"处理 {filepath} 时出错: {str(e)}")
    
    print(f"\n修复完成！共更新 {fixed_count} 个文件中的链接")

if __name__ == "__main__":
    fix_links()