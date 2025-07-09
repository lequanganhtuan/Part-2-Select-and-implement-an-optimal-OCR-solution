# PaddleOCR Evaluation Pipeline

## Mô tả

Dự án này xây dựng pipeline xử lý ảnh văn bản sử dụng **PaddleOCR** để nhận dạng chữ và đánh giá độ chính xác của kết quả bằng cách so sánh với ground truth. Hệ thống thực hiện:

1. Chạy OCR trên thư mục ảnh (`test_images/`)
2. Lưu kết quả dạng JSON (`output/`)
3. So sánh với ground truth (`*.gt.txt`) tương ứng
4. Tính **Precision**, **Recall**, và **F1-Score**

---

## Yêu cầu hệ thống

- Python 3.8+
- pip
- PaddleOCR (`paddleocr`)
- OpenCV (`opencv-python`)
- Pillow (`PIL`)

Cài đặt bằng lệnh:

```bash
pip install paddleocr paddlepaddle opencv-python pillow
```

---

## Cấu trúc thư mục

```bash
.
├── test_images/             # Thư mục chứa ảnh đầu vào + ground truth (*.gt.txt)
│   ├── doc1_en.png
│   ├── doc1_en.gt.txt
│   ├── doc2_fr.jpg
│   ├── doc2_fr.gt.txt
│   └── ...
├── output/                  # Thư mục chứa kết quả OCR (.json) (tự động tạo)
│   ├── doc1_en.json
│   └── ...
├── ocr_script.py           # Script chạy nhận dạng bằng PaddleOCR
├── evaluate.py             # Script đánh giá độ chính xác (precision, recall, F1)
└── README.md               # File hướng dẫn sử dụng
```

---

## Bước 1: Chạy OCR và xuất kết quả JSON

Sử dụng script `ocr_script.py` để nhận dạng chữ trong tất cả ảnh trong thư mục `test_images/`:

```bash
python ocr_script.py
```

Sau khi chạy thành công, bạn sẽ nhận được các file `.json` chứa kết quả nhận dạng được lưu tại thư mục `output/`.

**Ví dụ một file `doc1_en.json`:**

```json
[
  {
    "text": "HALTE",
    "confidence": 0.9861
  },
  {
    "text": "Guide de consultation",
    "confidence": 0.9896
  }
]
```

---

## Bước 2: Đánh giá chất lượng nhận dạng

Sau khi có kết quả nhận dạng, sử dụng script `evaluate.py` để đánh giá:

```bash
python evaluate.py
```

Script sẽ:

- Tìm các file `.gt.txt` tương ứng với ảnh
- So sánh nội dung ground truth với kết quả OCR
- Tính toán:
  - TP (True Positive)
  - FP (False Positive)
  - FN (False Negative)
  - Precision
  - Recall
  - F1 Score

**Ví dụ kết quả đầu ra:**

```
✅ doc1_en: TP=4, FP=74, FN=54

📊 Tổng Kết:
Precision: 5.13%
Recall:    6.90%
F1 Score:  5.88%
```

---

## 📝 Quy ước về ground truth

- Mỗi ảnh ví dụ `doc1_en.png` cần có file `doc1_en.gt.txt` tương ứng.
- File `.gt.txt` là file text chứa toàn bộ nội dung văn bản gốc của ảnh, được tách dòng nếu cần.
- Nội dung không cần format đặc biệt, chỉ cần đúng mặt chữ.
