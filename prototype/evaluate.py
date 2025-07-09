import os
import json
from difflib import SequenceMatcher

GT_DIR = 'ground_truth'  
OCR_DIR = 'output'       

def load_gt_lines(gt_path):
    with open(gt_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_ocr_lines(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [item['text'].strip() for item in data if item['text'].strip()]

def line_match(a, b, threshold=0.9):
    return SequenceMatcher(None, a, b).ratio() >= threshold

def evaluate_file(gt_lines, ocr_lines):
    TP = 0
    matched_ocr = set()
    for gt_line in gt_lines:
        found = False
        for idx, ocr_line in enumerate(ocr_lines):
            if idx in matched_ocr:
                continue
            if line_match(gt_line, ocr_line):
                TP += 1
                matched_ocr.add(idx)
                found = True
                break
    FP = len(ocr_lines) - len(matched_ocr)
    FN = len(gt_lines) - TP
    return TP, FP, FN

def main():
    total_TP = total_FP = total_FN = 0

    for filename in os.listdir(GT_DIR):
        if not filename.endswith('.gt.txt'):
            continue
        base = filename.replace('.gt.txt', '')
        gt_path = os.path.join(GT_DIR, filename)
        ocr_path = os.path.join(OCR_DIR, f'{base}.json')
        if not os.path.exists(ocr_path):
            print(f"Missing OCR result for {base}")
            continue

        gt_lines = load_gt_lines(gt_path)
        ocr_lines = load_ocr_lines(ocr_path)
        TP, FP, FN = evaluate_file(gt_lines, ocr_lines)
        total_TP += TP
        total_FP += FP
        total_FN += FN
        print(f"{base}: TP={TP}, FP={FP}, FN={FN}")

    precision = total_TP / (total_TP + total_FP) if (total_TP + total_FP) > 0 else 0
    recall    = total_TP / (total_TP + total_FN) if (total_TP + total_FN) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print("\n Summary:")
    print(f"Precision: {precision:.2%}")
    print(f"Recall:    {recall:.2%}")
    print(f"F1 Score:  {f1:.2%}")

if __name__ == '__main__':
    main()
