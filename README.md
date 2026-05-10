# Image to Text Extractor

An OCR (Optical Character Recognition) application that extracts text from images using Tesseract OCR engine with a user-friendly GUI.

## Author

**Paradorn Katananon**

## Features

- 📷 **Single Image Processing**: Extract text from individual images
- 📁 **Batch Processing**: Process multiple images in a folder at once
- ✏️ **Editable Preview**: Review and edit extracted text before saving
- 🌍 **Multi-language Support**: English, Chinese (Simplified/Traditional), Spanish, French, German, Japanese, Korean
- ⚙️ **Configurable OCR Settings**: Adjust page segmentation modes for better accuracy
- 💾 **Flexible Saving**: Save individual files or batch process with automatic file naming
- 🔄 **Responsive UI**: Multi-threaded processing keeps the interface responsive

## Requirements

- Python 3.x
- Tesseract OCR engine
- Required Python packages:
  - `pytesseract`
  - `Pillow (PIL)`
  - `tkinter` (usually included with Python)

## Installation

1. **Install Tesseract OCR**:
   - **Windows**: Download from [GitHub Tesseract Releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

2. **Install Python dependencies**:
   ```bash
   pip install pytesseract Pillow
   ```

3. **Configure Tesseract path** (if needed):
   If Tesseract is not in your system PATH, add this line to the code:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

## Usage

### Running the Application

```bash
python img2txt.py
```

### Single Image Mode

1. Click **"📷 Select Single Image"**
2. Choose an image file (PNG, JPG, JPEG, TIFF, BMP, GIF)
3. Review the extracted text in the preview area
4. Edit the text if needed
5. Click **"💾 Save Text to File"** to save

### Batch Processing Mode

1. Click **"📁 Select Folder (Batch)"**
2. Select a folder containing multiple images
3. All images will be processed automatically
4. Text files are saved in an `extracted_texts` subfolder
5. Review the processing summary

## OCR Settings

### Language Selection

Choose the appropriate language for better OCR accuracy:
- `eng` - English
- `chi_sim` - Chinese Simplified
- `chi_tra` - Chinese Traditional
- `spa` - Spanish
- `fra` - French
- `deu` - German
- `jpn` - Japanese
- `kor` - Korean

### Page Segmentation Modes

Select the page segmentation mode based on your image type:

- **PSM 3 (Auto)**: Fully automatic page segmentation. Best for general documents when you're unsure.
- **PSM 6 (Block)**: Single uniform block of text. Ideal for clean documents, books, single-column text.
- **PSM 11 (Sparse)**: Sparse text with no particular order. Good for screenshots, forms, receipts, or scattered text.
- **PSM 12 (Sparse + OSD)**: Sparse text with orientation and script detection. Same as PSM 11 but handles rotated text.

## Supported Image Formats

- PNG
- JPG/JPEG
- TIFF
- BMP
- GIF

## File Structure

```
img2txt/
├── img2txt.py          # Main application file
├── README.md           # This file
└── extracted_texts/    # Created automatically for batch processing
```

## Tips for Better OCR Results

1. **Use high-resolution images**: Better image quality = better text recognition
2. **Ensure good contrast**: Black text on white background works best
3. **Avoid skewed images**: Straighten images for better accuracy
4. **Choose correct language**: Select the language that matches your image text
5. **Adjust PSM mode**: Experiment with different segmentation modes for your specific use case

## Troubleshooting

### "Tesseract not found" error
- Ensure Tesseract OCR is installed
- Add Tesseract to your system PATH
- Or specify the path in the code

### Poor OCR accuracy
- Check image quality and resolution
- Try different page segmentation modes
- Ensure correct language is selected
- Pre-process images (enhance contrast, remove noise)

### Language not working
- Install additional Tesseract language packs
- Verify language data files are in Tesseract's `tessdata` folder

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Version

1.0

---

**Created by Paradorn Katananon**
