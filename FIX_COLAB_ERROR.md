# 🔧 Sửa lỗi "Dataset images not found" trên Google Colab

## ❌ Lỗi gặp phải:
```
FileNotFoundError: Dataset 'mydata.yaml' images not found, missing path '/content/datasets/dataset/images/val'
```

## 🎯 Nguyên nhân:
- YOLO đang tìm dataset ở đường dẫn sai
- File `mydata.yaml` có đường dẫn không đúng với cấu trúc thư mục Colab

## ✅ Cách sửa:

### **Phương pháp 1: Sửa trong Notebook (Khuyến nghị)**

Trong cell "Tạo file cấu hình dataset", thay đổi code thành:

```python
# Tạo file mydata.yaml với đường dẫn tuyệt đối
import os
current_dir = os.getcwd()
dataset_path = os.path.join(current_dir, 'dataset')

yaml_content = f"""
# Dataset configuration for License Plate Detection
path: {dataset_path}  # dataset root dir (absolute path)
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

print(f"Đã tạo file mydata.yaml với đường dẫn: {dataset_path}")
```

### **Phương pháp 2: Kiểm tra và sửa thủ công**

Thêm cell này trước khi training:

```python
# Kiểm tra và sửa đường dẫn dataset
import os
import yaml

# Đọc file mydata.yaml hiện tại
with open('mydata.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Cập nhật đường dẫn
current_dir = os.getcwd()
config['path'] = os.path.join(current_dir, 'dataset')

# Ghi lại file
with open('mydata.yaml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False)

print(f"✅ Đã cập nhật đường dẫn dataset: {config['path']}")

# Kiểm tra đường dẫn
train_path = os.path.join(config['path'], config['train'])
val_path = os.path.join(config['path'], config['val'])

print(f"Train path: {train_path} - {'✅ Exists' if os.path.exists(train_path) else '❌ Not found'}")
print(f"Val path: {val_path} - {'✅ Exists' if os.path.exists(val_path) else '❌ Not found'}")
```

### **Phương pháp 3: Sử dụng đường dẫn tuyệt đối**

```python
# Tạo file mydata.yaml với đường dẫn tuyệt đối cố định
yaml_content = """
path: /content/license_plate_detection/dataset
train: images/train
val: images/val
test:

names:
  0: Bien_So

nc: 1
"""

with open('mydata.yaml', 'w') as f:
    f.write(yaml_content)
```

## 🔍 Debug steps:

### **1. Kiểm tra thư mục hiện tại:**
```python
import os
print(f"Current directory: {os.getcwd()}")
print(f"Files in current dir: {os.listdir('.')}")
```

### **2. Kiểm tra cấu trúc dataset:**
```python
def check_dataset():
    paths_to_check = [
        'dataset',
        'dataset/images',
        'dataset/images/train',
        'dataset/images/val',
        'dataset/labels',
        'dataset/labels/train',
        'dataset/labels/val'
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            count = len(os.listdir(path)) if os.path.isdir(path) else 0
            print(f"✅ {path}: {count} items")
        else:
            print(f"❌ {path}: Not found")

check_dataset()
```

### **3. Kiểm tra nội dung mydata.yaml:**
```python
with open('mydata.yaml', 'r') as f:
    print("📄 mydata.yaml content:")
    print(f.read())
```

## 🚀 Notebook đã được cập nhật:

File `train_license_plate_colab.ipynb` đã được cập nhật với:
- ✅ Tự động tạo đường dẫn đúng
- ✅ Kiểm tra dataset trước khi training
- ✅ Validation dataset trước khi bắt đầu
- ✅ Error handling tốt hơn

## 💡 Tips:

1. **Luôn kiểm tra đường dẫn** trước khi training
2. **Sử dụng đường dẫn tuyệt đối** để tránh lỗi
3. **Kiểm tra cấu trúc dataset** trước khi upload
4. **Backup dataset** trên Google Drive

## 📞 Nếu vẫn gặp lỗi:

1. Restart runtime: `Runtime → Restart runtime`
2. Chạy lại từ đầu
3. Kiểm tra quota GPU còn lại
4. Thử với model nhỏ hơn: `yolov8n.pt` thay vì `yolov8x.pt`

---

**Chúc bạn training thành công! 🎉**
