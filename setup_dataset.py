#!/usr/bin/env python3
"""
Script để setup dataset cho training
Tự động giải nén và tổ chức dataset
"""

import os
import zipfile
import shutil
from pathlib import Path

def find_zip_files():
    """Tìm tất cả file zip trong thư mục hiện tại"""
    zip_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.zip'):
                zip_files.append(os.path.join(root, file))
    return zip_files

def extract_zip_file(zip_path, extract_to='.'):
    """Giải nén file zip"""
    print(f"📦 Giải nén {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ Đã giải nén {zip_path}")
        return True
    except Exception as e:
        print(f"❌ Lỗi giải nén {zip_path}: {e}")
        return False

def find_dataset_structure():
    """Tìm thư mục chứa images và labels"""
    for root, dirs, files in os.walk('.'):
        if 'images' in dirs and 'labels' in dirs:
            return root
    return None

def organize_dataset(source_dir):
    """Tổ chức dataset vào cấu trúc chuẩn"""
    print(f"📁 Tổ chức dataset từ {source_dir}...")
    
    # Tạo thư mục dataset chính
    dataset_dir = Path('dataset')
    dataset_dir.mkdir(exist_ok=True)
    
    source_path = Path(source_dir)
    
    # Di chuyển images
    source_images = source_path / 'images'
    target_images = dataset_dir / 'images'
    
    if source_images.exists():
        if target_images.exists():
            shutil.rmtree(target_images)
        shutil.copytree(source_images, target_images)
        print(f"✅ Đã copy thư mục images")
    
    # Di chuyển labels
    source_labels = source_path / 'labels'
    target_labels = dataset_dir / 'labels'
    
    if source_labels.exists():
        if target_labels.exists():
            shutil.rmtree(target_labels)
        shutil.copytree(source_labels, target_labels)
        print(f"✅ Đã copy thư mục labels")

def check_dataset_structure():
    """Kiểm tra cấu trúc dataset sau khi setup"""
    print("\n🔍 Kiểm tra cấu trúc dataset...")
    
    required_dirs = [
        'dataset/images/train',
        'dataset/images/val',
        'dataset/labels/train', 
        'dataset/labels/val'
    ]
    
    all_good = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            files = [f for f in os.listdir(dir_path) 
                    if f.endswith(('.jpg', '.png', '.jpeg', '.txt'))]
            file_count = len(files)
            print(f"✅ {dir_path}: {file_count} files")
            if file_count == 0:
                print(f"   ⚠️  Thư mục trống!")
                all_good = False
        else:
            print(f"❌ {dir_path}: Không tồn tại")
            all_good = False
    
    return all_good

def create_yaml_config():
    """Tạo file cấu hình mydata.yaml"""
    yaml_content = """# Dataset configuration for License Plate Detection
path: ./dataset  # dataset root dir
train: images/train  # train images (relative to 'path')
val: images/val  # val images (relative to 'path')
test:  # test images (optional)

# Classes
names:
  0: Bien_So

# Number of classes
nc: 1
"""
    
    with open('mydata.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    print("✅ Đã tạo file mydata.yaml")

def main():
    """Main function"""
    print("🚗 Dataset Setup for License Plate Detection")
    print("=" * 50)
    
    # Kiểm tra xem dataset đã có chưa
    if check_dataset_structure():
        print("🎉 Dataset đã sẵn sàng!")
        create_yaml_config()
        return
    
    print("📦 Tìm kiếm file zip...")
    zip_files = find_zip_files()
    
    if not zip_files:
        print("❌ Không tìm thấy file zip nào!")
        print("💡 Hãy đảm bảo có file dataset.zip trong thư mục")
        return
    
    print(f"📁 Tìm thấy {len(zip_files)} file zip:")
    for zip_file in zip_files:
        print(f"   - {zip_file}")
    
    # Giải nén tất cả file zip
    for zip_file in zip_files:
        extract_zip_file(zip_file)
    
    # Tìm thư mục dataset
    dataset_source = find_dataset_structure()
    
    if dataset_source:
        print(f"📁 Tìm thấy dataset tại: {dataset_source}")
        
        # Nếu không phải ở ./dataset, tổ chức lại
        if dataset_source != './dataset' and dataset_source != 'dataset':
            organize_dataset(dataset_source)
        
        # Kiểm tra lại
        if check_dataset_structure():
            print("\n🎉 Dataset setup thành công!")
            create_yaml_config()
            
            print("\n💡 Bước tiếp theo:")
            print("1. Chạy: python test_dataset.py (để kiểm tra)")
            print("2. Chạy: python main.py (để train local)")
            print("3. Hoặc upload lên Colab để train với GPU")
        else:
            print("\n❌ Dataset setup thất bại!")
    else:
        print("❌ Không tìm thấy thư mục dataset hợp lệ!")
        print("💡 Đảm bảo file zip chứa thư mục 'images' và 'labels'")

if __name__ == "__main__":
    main()
