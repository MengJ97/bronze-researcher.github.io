import os
import re
import shutil

def clean_filename(name):
    """清理文件名中的特殊字符"""
    # 移除首尾单引号
    name = name.strip("'")
    # 替换特殊字符
    name = re.sub(r'[^\w\-\.]', '_', name)
    # 缩短过长文件名
    return name[:120] + '.html'

def fix_individuals_files():
    """修复 individuals 目录中的文件名"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    individuals_dir = os.path.join(base_dir, 'individuals')
    
    if not os.path.exists(individuals_dir):
        print(f"错误：目录不存在 - {individuals_dir}")
        return
    
    print(f"正在修复 {individuals_dir} 中的文件...")
    count = 0
    
    # 创建备份目录
    backup_dir = os.path.join(base_dir, 'individuals_backup')
    os.makedirs(backup_dir, exist_ok=True)
    
    for filename in os.listdir(individuals_dir):
        if filename.endswith('.html'):
            # 清理文件名
            clean_name = clean_filename(filename)
            
            if clean_name != filename:
                # 原始文件路径
                old_path = os.path.join(individuals_dir, filename)
                # 新文件路径
                new_path = os.path.join(individuals_dir, clean_name)
                
                # 备份原始文件
                shutil.copy2(old_path, os.path.join(backup_dir, filename))
                
                # 重命名文件
                os.rename(old_path, new_path)
                print(f"重命名: {filename} -> {clean_name}")
                count += 1
    
    print(f"\n完成！修复了 {count} 个文件")
    print(f"原始文件已备份至: {backup_dir}")
    print("请手动检查以下内容：")
    print("1. 检查所有链接是否工作正常")
    print("2. 提交更改到 Git 仓库")
    print("3. 推送到 GitHub")

if __name__ == "__main__":
    fix_individuals_files()