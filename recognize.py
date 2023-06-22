from paddleocr import PaddleOCR, draw_ocr

# Use English language, you can switch to Chinese by changing 'en' to 'ch'
ocr = PaddleOCR(use_gpu=False, lang="en") 
img_path = 'pic2.png'
result = ocr.ocr(img_path, use_gpu=False)

for line in result:
    line_text = ' '.join([word_info[-1] for word_info in line])
    print(line_text)
