# 🚗 Hướng dẫn chạy Training Nhận diện Biển số xe trên Google Colab

## 📋 Tổng quan
Project này sử dụng YOLOv8 để train model nhận diện biển số xe trên Google Colab với GPU miễn phí.

## 🚀 Cách sử dụng

### Phương pháp 1: Sử dụng GitHub (Khuyến nghị)

1. **Upload project lên GitHub:**
   ```bash
   # Tạo repo mới trên GitHub
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/NhanDienBSX.git
   git push -u origin main
   ```

2. **Mở Colab và chạy:**
   - Truy cập: https://colab.research.google.com/
   - File → Open notebook → GitHub
   - Nhập URL: `https://github.com/YOUR_USERNAME/NhanDienBSX/blob/main/train_license_plate_colab.ipynb`
   - Hoặc upload file `train_license_plate_colab.ipynb` trực tiếp

3. **Sửa code trong notebook:**
   - Tìm cell "Clone từ GitHub"
   - Uncomment và sửa dòng:
   ```python
   !git clone https://github.com/YOUR_USERNAME/NhanDienBSX.git
   os.chdir('NhanDienBSX')
   ```

### Phương pháp 2: Upload thủ công

1. **Chuẩn bị files:**
   - Nén thư mục `dataset` thành `dataset.zip`
   - Chuẩn bị file `mydata.yaml`

2. **Upload lên Colab:**
   - Upload file `train_license_plate_colab.ipynb`
   - Chạy từng cell theo thứ tự
   - Upload files khi được yêu cầu

## 📁 Cấu trúc Dataset cần thiết

```
dataset/
├── images/
│   ├── train/          # Ảnh training
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   └── val/            # Ảnh validation
│       ├── img1.jpg
│       ├── img2.jpg
│       └── ...
└── labels/
    ├── train/          # Label training (YOLO format)
    │   ├── img1.txt
    │   ├── img2.txt
    │   └── ...
    └── val/            # Label validation
        ├── img1.txt
        ├── img2.txt
        └── ...
```

## ⚙️ Cấu hình Training

Trong notebook, bạn có thể điều chỉnh các tham số:

```python
EPOCHS = 50          # Số epochs (có thể tăng lên 100-200)
IMG_SIZE = 640       # Kích thước ảnh
BATCH_SIZE = 16      # Batch size (giảm nếu bị out of memory)
```

## 🎯 Model YOLO có thể chọn

- `yolov8n.pt` - Nano (nhanh nhất, nhẹ nhất)
- `yolov8s.pt` - Small 
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (chính xác nhất, nặng nhất)

## 📊 Kết quả Training

Sau khi training xong, bạn sẽ có:

1. **Model file:** `best.pt` - Model tốt nhất
2. **Biểu đồ:** 
   - `results.png` - Loss và metrics
   - `confusion_matrix.png` - Ma trận nhầm lẫn
   - `train_batch0.png` - Ảnh training sample
   - `val_batch0_pred.png` - Kết quả prediction

3. **Files download:**
   - `license_plate_model.zip` - Toàn bộ kết quả
   - `best_license_plate_model.pt` - Model tốt nhất

## 🔧 Troubleshooting

### Lỗi Out of Memory:
```python
BATCH_SIZE = 8  # Giảm batch size
# Hoặc chọn model nhỏ hơn
model = YOLO("yolov8n.pt")  # Thay vì yolov8x.pt
```

### Lỗi Dataset không tìm thấy:
- Kiểm tra cấu trúc thư mục
- Đảm bảo file `mydata.yaml` đúng đường dẫn

### GPU không hoạt động:
- Runtime → Change runtime type → Hardware accelerator → GPU

## 📱 Sử dụng Model sau khi train

```python
from ultralytics import YOLO

# Load model đã train
model = YOLO('best_license_plate_model.pt')

# Predict trên ảnh mới
results = model('path/to/new_image.jpg')

# Hiển thị kết quả
results[0].show()

# Lưu kết quả
results[0].save('result.jpg')
```

## 🎉 Lưu ý quan trọng

1. **GPU Runtime:** Colab miễn phí có giới hạn GPU (~12 giờ/ngày)
2. **Lưu trữ:** Luôn lưu kết quả vào Google Drive
3. **Backup:** Download model về máy để backup
4. **Dataset:** Đảm bảo dataset có chất lượng tốt và đủ lớn

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Cấu trúc dataset
2. File `mydata.yaml`
3. GPU có được bật không
4. Dung lượng RAM/Storage

---

**Chúc bạn training thành công! 🚀**
