import os
import sys
import argparse
from pathlib import Path

# Monkey-patch paddle config for PaddleOCR 3.4/Paddle 2.6+ compatibility
try:
    import paddle
    import paddle.base.libpaddle
    if not hasattr(paddle.base.libpaddle.AnalysisConfig, 'set_optimization_level'):
        paddle.base.libpaddle.AnalysisConfig.set_optimization_level = lambda self, x: None
except ImportError:
    pass

def process_directory(directory_path, output_path, lang):
    dir_path = Path(directory_path)
    if not dir_path.exists() or not dir_path.is_dir():
        print(f"Error: Directory {directory_path} does not exist.")
        sys.exit(1)
        
    print(f"Scanning directory: {directory_path}")
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
    
    # Get all images and sort them alphabetically
    image_files = []
    for file in dir_path.iterdir():
        if file.suffix.lower() in image_extensions:
            image_files.append(file)
            
    image_files.sort(key=lambda x: x.name)
    
    if not image_files:
        print(f"No images found in {directory_path}")
        sys.exit(1)
        
    print(f"Found {len(image_files)} images, loading OCR model for lang={lang}...")
    
    if lang == 'ja':
        try:
            from manga_ocr import MangaOcr
            mocr = MangaOcr()
            def do_ocr(img_path):
                return mocr(str(img_path))
        except ImportError:
            print("Error: manga_ocr is not installed. Run: pip install manga-ocr")
            sys.exit(1)
            
    elif lang in ['cn', 'en']:
        try:
            import easyocr
            use_lang = ['ch_sim', 'en'] if lang == 'cn' else ['en']
            # Initialize the EasyOCR reader (gpu=True by default)
            reader = easyocr.Reader(use_lang, gpu=True)
            def do_ocr(img_path):
                # Returns list of tuples (bbox, text, prob)
                result = reader.readtext(str(img_path))
                if not result:
                    return ""
                return "\n".join([item[1] for item in result])
        except ImportError:
            print("Error: easyocr not installed. Run: pip install easyocr")
            sys.exit(1)
    else:
        print(f"Error: Unsupported language '{lang}'")
        sys.exit(1)
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write(f"# Raw OCR Dump\n")
        out_file.write(f"**Source Directory**: `{directory_path}`\n\n")
        
        for img_path in image_files:
            print(f"Processing: {img_path.name}")
            try:
                text = do_ocr(img_path)
                out_file.write(f"## Page: {img_path.name}\n")
                out_file.write(f"{text}\n\n")
            except Exception as e:
                print(f"Error processing {img_path.name}: {e}")
                out_file.write(f"## Page: {img_path.name}\n")
                out_file.write(f"*[OCR Error: {e}]*\n\n")
                
    print(f"\nBatch OCR completed successfully! Dump saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch process manga pages with universal OCR.")
    parser.add_argument("--dir", required=True, help="Directory containing manga images.")
    parser.add_argument("--out", required=True, help="Output markdown file path.")
    parser.add_argument("--lang", default="ja", choices=["ja", "cn", "en"], help="Target language (ja/cn/en)")
    
    args = parser.parse_args()
    process_directory(args.dir, args.out, args.lang)

