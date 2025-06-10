#!/usr/bin/env python3
"""
Script để test dataset trước khi training trên Colab
"""

import os
import yaml
from pathlib import Path

def check_dataset_structure():
    """Kiểm tra cấu trúc dataset"""
    print("🔍 Kiểm tra cấu trúc dataset...")
    
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

def check_image_label_correspondence():
    """Kiểm tra tương ứng giữa images và labels"""
    print("\n📊 Kiểm tra tương ứng images-labels...")
    
    # Train set
    train_img_dir = Path('dataset/images/train')
    train_lbl_dir = Path('dataset/labels/train')
    
    if train_img_dir.exists() and train_lbl_dir.exists():
        train_images = {f.stem for f in train_img_dir.glob('*') 
                       if f.suffix.lower() in ['.jpg', '.png', '.jpeg']}
        train_labels = {f.stem for f in train_lbl_dir.glob('*.txt')}
        
        print(f"Train: {len(train_images)} images, {len(train_labels)} labels")
        
        missing_labels = train_images - train_labels
        missing_images = train_labels - train_images
        
        if missing_labels:
            print(f"   ⚠️  Missing labels: {list(missing_labels)[:5]}...")
        if missing_images:
            print(f"   ⚠️  Missing images: {list(missing_images)[:5]}...")
    
    # Val set
    val_img_dir = Path('dataset/images/val')
    val_lbl_dir = Path('dataset/labels/val')
    
    if val_img_dir.exists() and val_lbl_dir.exists():
        val_images = {f.stem for f in val_img_dir.glob('*') 
                     if f.suffix.lower() in ['.jpg', '.png', '.jpeg']}
        val_labels = {f.stem for f in val_lbl_dir.glob('*.txt')}
        
        print(f"Val: {len(val_images)} images, {len(val_labels)} labels")
        
        missing_labels = val_images - val_labels
        missing_images = val_labels - val_images
        
        if missing_labels:
            print(f"   ⚠️  Missing labels: {list(missing_labels)[:5]}...")
        if missing_images:
            print(f"   ⚠️  Missing images: {list(missing_images)[:5]}...")

def check_yaml_config():
    """Kiểm tra file cấu hình YAML"""
    print("\n📄 Kiểm tra file mydata.yaml...")
    
    if not os.path.exists('mydata.yaml'):
        print("❌ File mydata.yaml không tồn tại!")
        return False
    
    try:
        with open('mydata.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print(f"✅ File YAML hợp lệ")
        print(f"   Path: {config.get('path', 'N/A')}")
        print(f"   Train: {config.get('train', 'N/A')}")
        print(f"   Val: {config.get('val', 'N/A')}")
        print(f"   Classes: {config.get('names', 'N/A')}")
        
        # Kiểm tra đường dẫn
        dataset_path = config.get('path', '')
        if dataset_path.startswith('./'):
            dataset_path = dataset_path[2:]
        
        train_path = os.path.join(dataset_path, config.get('train', ''))
        val_path = os.path.join(dataset_path, config.get('val', ''))
        
        if os.path.exists(train_path):
            print(f"✅ Train path exists: {train_path}")
        else:
            print(f"❌ Train path not found: {train_path}")
            
        if os.path.exists(val_path):
            print(f"✅ Val path exists: {val_path}")
        else:
            print(f"❌ Val path not found: {val_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi đọc file YAML: {e}")
        return False

def check_label_format():
    """Kiểm tra format của label files"""
    print("\n🏷️  Kiểm tra format labels...")
    
    label_files = list(Path('dataset/labels/train').glob('*.txt'))[:3]  # Check first 3 files
    
    for label_file in label_files:
        print(f"\n📝 Checking {label_file.name}:")
        try:
            with open(label_file, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines[:3]):  # Check first 3 lines
                parts = line.strip().split()
                if len(parts) >= 5:
                    class_id, x, y, w, h = parts[:5]
                    print(f"   Line {i+1}: class={class_id}, x={x}, y={y}, w={w}, h={h}")
                    
                    # Validate values
                    try:
                        cls = int(class_id)
                        x_val, y_val, w_val, h_val = map(float, [x, y, w, h])
                        
                        if not (0 <= x_val <= 1 and 0 <= y_val <= 1 and 
                               0 <= w_val <= 1 and 0 <= h_val <= 1):
                            print(f"   ⚠️  Coordinates out of range [0,1]")
                    except ValueError:
                        print(f"   ❌ Invalid number format")
                else:
                    print(f"   ❌ Invalid format: {line.strip()}")
                    
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")

def main():
    """Main function"""
    print("🚗 Dataset Validation for License Plate Detection")
    print("=" * 50)
    
    # Check current directory
    print(f"📁 Current directory: {os.getcwd()}")
    
    # Run all checks
    structure_ok = check_dataset_structure()
    check_image_label_correspondence()
    yaml_ok = check_yaml_config()
    check_label_format()
    
    print("\n" + "=" * 50)
    if structure_ok and yaml_ok:
        print("🎉 Dataset validation PASSED! Sẵn sàng cho training.")
    else:
        print("❌ Dataset validation FAILED! Cần sửa lỗi trước khi training.")
    
    print("\n💡 Để chạy trên Colab:")
    print("1. Upload notebook 'train_license_plate_colab.ipynb'")
    print("2. Upload dataset hoặc clone từ GitHub")
    print("3. Chạy từng cell theo thứ tự")

if __name__ == "__main__":
    main()
