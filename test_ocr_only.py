import cv2
import easyocr
import sys
import os
import numpy as np

def test_single_image_ocr(image_path):
    print(f"🔍 Test OCR trên ảnh: {image_path}")

    # Kiểm tra file tồn tại
    if not os.path.exists(image_path):
        print(f"❌ File không tồn tại: {image_path}")
        return

    # Khởi tạo EasyOCR
    try:
        reader = easyocr.Reader(['en'], gpu=False)
        print("✅ EasyOCR đã sẵn sàng")
    except Exception as e:
        print(f"❌ Lỗi EasyOCR: {e}")
        return

    # Đọc ảnh
    img = cv2.imread(image_path)
    if img is None:
        print("❌ Không đọc được ảnh")
        return

    print(f"📐 Kích thước ảnh: {img.shape[1]}x{img.shape[0]}")

    try:
        # Test OCR trên toàn bộ ảnh
        print("🔍 Đang chạy OCR...")
        results = reader.readtext(img)

        detected_plates = []

        if results:
            print(f"✅ Tìm thấy {len(results)} vùng text:")

            for i, (bbox, text, confidence) in enumerate(results):
                print(f"   {i+1}. Text: '{text}' (confidence: {confidence:.3f})")

                # Lọc text có thể là biển số
                clean_text = text.replace(" ", "").replace("-", "").upper()
                if len(clean_text) >= 4 and confidence > 0.5:
                    # Kiểm tra pattern biển số VN (có số và chữ)
                    has_digit = any(c.isdigit() for c in clean_text)
                    has_letter = any(c.isalpha() for c in clean_text)

                    if has_digit and (has_letter or len(clean_text) >= 5):
                        detected_plates.append(clean_text)
                        print(f"      🎯 Có thể là biển số: {clean_text}")

            if detected_plates:
                print(f"🏆 BIỂN SỐ PHÁT HIỆN: {', '.join(detected_plates)}")
            else:
                print("⚠️ Không tìm thấy pattern biển số")
        else:
            print("❌ Không phát hiện text nào")

        # Tạo ảnh kết quả
        result_img = img.copy()

        # Vẽ tất cả text được phát hiện
        if results:
            for (bbox, text, confidence) in results:
                if confidence > 0.3:
                    # Vẽ bounding box
                    points = np.array(bbox, dtype=np.int32)
                    cv2.polylines(result_img, [points], True, (0, 255, 0), 3)

                    # Vẽ text với background
                    x, y = points[0]

                    # Tính kích thước text
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 1.2
                    thickness = 3
                    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

                    # Vẽ background đen cho text
                    cv2.rectangle(result_img,
                                (x - 5, y - text_size[1] - 15),
                                (x + text_size[0] + 5, y + 5),
                                (0, 0, 0), -1)

                    # Vẽ border trắng
                    cv2.rectangle(result_img,
                                (x - 5, y - text_size[1] - 15),
                                (x + text_size[0] + 5, y + 5),
                                (255, 255, 255), 2)

                    # Vẽ text màu xanh lá
                    cv2.putText(result_img, text, (x, y), font, font_scale, (0, 255, 0), thickness)

                    # Vẽ confidence score nhỏ hơn
                    conf_text = f"({confidence:.2f})"
                    cv2.putText(result_img, conf_text,
                              (x + text_size[0] + 10, y),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        # Hiển thị biển số được phát hiện ở góc trên
        if detected_plates:
            plates_text = f"BIEN SO: {', '.join(detected_plates)}"
            # Background cho text biển số
            text_size = cv2.getTextSize(plates_text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
            cv2.rectangle(result_img, (10, 10), (text_size[0] + 20, 50), (0, 0, 0), -1)
            cv2.rectangle(result_img, (10, 10), (text_size[0] + 20, 50), (0, 255, 0), 2)
            cv2.putText(result_img, plates_text, (15, 35),
                      cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            
        # Hiển thị ảnh với GUI
        print(f"\n🖼️ Hiển thị ảnh với kết quả OCR...")
        print("📋 Điều khiển:")
        print("   - ESC hoặc Q: Thoát")
        print("   - S: Lưu ảnh kết quả")

        # Resize ảnh nếu quá lớn để hiển thị
        display_img_resized = result_img.copy()
        height, width = display_img_resized.shape[:2]
        if width > 1200 or height > 800:
            scale = min(1200/width, 800/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            display_img_resized = cv2.resize(display_img_resized, (new_width, new_height))

        # Hiển thị ảnh
        cv2.imshow('License Plate OCR Result', display_img_resized)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):  # ESC hoặc Q
                break
            elif key == ord('s'):  # S để lưu
                result_path = f"ocr_result_{os.path.basename(image_path)}"
                cv2.imwrite(result_path, result_img)
                print(f"💾 Đã lưu: {result_path}")

        cv2.destroyAllWindows()

    except Exception as e:
        print(f"❌ Lỗi xử lý: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_single_image_ocr(image_path)
    else:
        print("❌ Cách sử dụng: python test_ocr_only.py <đường_dẫn_ảnh>")
        print("📝 Ví dụ: python test_ocr_only.py kq.jpg")
        print("📝 Ví dụ: python test_ocr_only.py dataset/images/train/abc.jpg")
