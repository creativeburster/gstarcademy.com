import os
import shutil

def prepare_dist():
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)

    # 1. 复制根目录下的静态资源
    allowed_extensions = {".html", ".js", ".css", ".json", ".xml", ".svg", ".txt"}
    for item in os.listdir("."):
        if os.path.isfile(item):
            ext = os.path.splitext(item)[1].lower()
            if ext in allowed_extensions or item in {"_redirects", "_headers"}:
                print(f"Copying {item} to dist/")
                shutil.copy(item, os.path.join(dist_dir, item))

    # 2. 复制 data 目录
    data_dist = os.path.join(dist_dir, "data")
    os.makedirs(data_dist)
    for root, dirs, files in os.walk("data"):
        # 计算相对路径
        rel_path = os.path.relpath(root, "data")
        target_dir = data_dist if rel_path == "." else os.path.join(data_dist, rel_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for f in files:
            src_file = os.path.join(root, f)
            print(f"Copying {src_file} to {target_dir}")
            shutil.copy(src_file, os.path.join(target_dir, f))

    # 3. 复制 images 目录
    images_dist = os.path.join(dist_dir, "images")
    os.makedirs(images_dist)
    for root, dirs, files in os.walk("images"):
        rel_path = os.path.relpath(root, "images")
        target_dir = images_dist if rel_path == "." else os.path.join(images_dist, rel_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for f in files:
            src_file = os.path.join(root, f)
            shutil.copy(src_file, os.path.join(target_dir, f))

    # 4. 复制 kb 目录
    kb_dist = os.path.join(dist_dir, "kb")
    os.makedirs(kb_dist)
    for root, dirs, files in os.walk("kb"):
        rel_path = os.path.relpath(root, "kb")
        target_dir = kb_dist if rel_path == "." else os.path.join(kb_dist, rel_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for f in files:
            src_file = os.path.join(root, f)
            shutil.copy(src_file, os.path.join(target_dir, f))

    print("Dist directory prepared successfully!")

if __name__ == "__main__":
    prepare_dist()
