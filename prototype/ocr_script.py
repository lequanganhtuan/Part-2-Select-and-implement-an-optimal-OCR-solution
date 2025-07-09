from paddleocr import PaddleOCR
import os
import json

ocr = PaddleOCR(use_textline_orientation=True, lang='en')

INPUT_DIR = 'test_images'
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_ocr_on_image(image_path):
    result = ocr.predict(image_path)  

    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
        texts = result[0].get('rec_texts', [])
        scores = result[0].get('rec_scores', [])
    else:
        print(f" Unexpected result format for: {image_path}")
        return []

    lines = []
    for text, score in zip(texts, scores):
        lines.append({
            "text": text,
            "confidence": score
        })

    return lines

def save_ocr_result_to_json(image_path, result):
    base_name = os.path.basename(image_path)
    file_id = os.path.splitext(base_name)[0]
    output_path = os.path.join(OUTPUT_DIR, f"{file_id}.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def main():
    print(f" Running OCR on folder: {INPUT_DIR}")
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {filename}")
            try:
                result = run_ocr_on_image(img_path)
                save_ocr_result_to_json(img_path, result)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    print(f"\nOCR completed. Results saved in: {OUTPUT_DIR}/")

if __name__ == '__main__':
    main()
