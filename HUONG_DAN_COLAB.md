# 🚗 Hướng dẫn Training Nhận diện Biển số xe trên Google Colab

## 📋 Tổng quan
Project này sử dụng YOLOv8 để train model nhận diện biển số xe. Bạn có thể train trên Google Colab miễn phí với GPU Tesla T4.

## 🎯 Dataset hiện tại
- **Train:** 8 images + 8 labels
- **Val:** 4 images + 4 labels  
- **Format:** YOLO (class x y w h)
- **Class:** 0 = Bien_So

## 🚀 Cách 1: Upload trực tiếp lên Colab (Đơn giản nhất)

### Bước 1: Chuẩn bị files
```bash
# Nén dataset thành zip
zip -r dataset.zip dataset/

# Hoặc trên Windows
# Chuột phải dataset → Send to → Compressed folder
```

### Bước 2: Mở Colab
1. Truy cập: https://colab.research.google.com/
2. File → Upload notebook
3. Chọn file `train_license_plate_colab.ipynb`

### Bước 3: Chạy training
1. **Cell 1:** Cài đặt thư viện
2. **Cell 2:** Mount Google Drive (tùy chọn)
3. **Cell 3:** Bỏ qua (dành cho GitHub)
4. **Cell 4:** Upload file `dataset.zip` khi được yêu cầu
5. **Cell 5-10:** Chạy lần lượt để training

## 🚀 Cách 2: Sử dụng GitHub (Khuyến nghị)

### Bước 1: Upload lên GitHub
```bash
# Thêm files mới
git add .
git commit -m "Add Colab training setup"
git push origin main
```

### Bước 2: Mở từ GitHub
1. Vào Colab: https://colab.research.google.com/
2. File → Open notebook → GitHub
3. Nhập URL repo: `https://github.com/YOUR_USERNAME/NhanDienBSX`
4. Chọn `train_license_plate_colab.ipynb`

### Bước 3: Sửa code clone
Trong cell "Clone từ GitHub", sửa:
```python
# Uncomment và sửa dòng này
!git clone https://github.com/YOUR_USERNAME/NhanDienBSX.git
%cd NhanDienBSX
```

## ⚙️ Cấu hình Training

### Tham số có thể điều chỉnh:
```python
EPOCHS = 50          # Số epochs (50-200)
IMG_SIZE = 640       # Kích thước ảnh
BATCH_SIZE = 16      # Batch size (giảm nếu out of memory)
```

### Model size options:
- `yolov8n.pt` - Nano (nhanh, nhẹ)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium  
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (chính xác nhất)

## 📊 Kết quả Training

Sau khi training xong, bạn sẽ có:

### Files download tự động:
- `license_plate_model.zip` - Toàn bộ kết quả
- `best_license_plate_model.pt` - Model tốt nhất

### Biểu đồ training:
- `results.png` - Loss và metrics
- `confusion_matrix.png` - Ma trận nhầm lẫn
- `train_batch0.png` - Ảnh training sample
- `val_batch0_pred.png` - Kết quả prediction

### Lưu trên Google Drive:
- `/content/drive/MyDrive/license_plate_detection_results/`

## 🔧 Troubleshooting

### ❌ Lỗi "Dataset images not found"
**Nguyên nhân:** Đường dẫn dataset không đúng

**Giải pháp:** Notebook đã được cập nhật để tự động sửa lỗi này

### ❌ Lỗi "Out of Memory"
```python
# Giảm batch size
BATCH_SIZE = 8

# Hoặc dùng model nhỏ hơn
model = YOLO("yolov8n.pt")
```

### ❌ GPU không hoạt động
1. Runtime → Change runtime type
2. Hardware accelerator → GPU
3. Save

### ❌ Dataset không tìm thấy
1. Kiểm tra file zip đã upload đúng chưa
2. Đảm bảo cấu trúc: `dataset/images/train`, `dataset/images/val`
3. Chạy lại cell kiểm tra dataset

## 📱 Sử dụng Model sau Training

### Load model:
```python
from ultralytics import YOLO

# Load model đã train
model = YOLO('best_license_plate_model.pt')

# Predict trên ảnh mới
results = model('path/to/image.jpg')

# Hiển thị kết quả
results[0].show()

# Lưu kết quả
results[0].save('result.jpg')
```

### Predict batch:
```python
# Predict nhiều ảnh
results = model(['img1.jpg', 'img2.jpg', 'img3.jpg'])

for i, result in enumerate(results):
    result.save(f'result_{i}.jpg')
```

## 💡 Tips quan trọng

### 🕐 Giới hạn Colab:
- **GPU miễn phí:** ~12 giờ/ngày
- **RAM:** 12GB
- **Storage:** 100GB (tạm thời)

### 💾 Backup quan trọng:
1. **Luôn lưu vào Google Drive**
2. **Download model về máy**
3. **Commit code lên GitHub**

### 📈 Cải thiện model:
1. **Thêm data:** Càng nhiều ảnh càng tốt
2. **Data augmentation:** Đã tự động trong YOLO
3. **Tăng epochs:** 100-200 epochs cho kết quả tốt hơn
4. **Fine-tuning:** Điều chỉnh learning rate

## 📞 Hỗ trợ

### Kiểm tra trước khi training:
```bash
# Local testing
python setup_dataset.py    # Setup dataset
python test_dataset.py     # Kiểm tra dataset
python main.py             # Train local (nếu có GPU)
```

### Files quan trọng:
- `train_license_plate_colab.ipynb` - Notebook chính
- `mydata.yaml` - Cấu hình dataset
- `setup_dataset.py` - Setup dataset local
- `test_dataset.py` - Kiểm tra dataset
- `FIX_COLAB_ERROR.md` - Sửa lỗi thường gặp

---

## 🎉 Chúc bạn training thành công!

**Thời gian training dự kiến:** 30-60 phút (50 epochs với dataset nhỏ)

**Kết quả mong đợi:** Model có thể detect biển số xe với độ chính xác cao
