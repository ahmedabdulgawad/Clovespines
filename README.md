# Clovespines

#### Video Demo:  https://youtu.be/_IRHpRj0kmY

#### Description:
This project is an OCR (Optical Character Recognition) pipeline designed to process PDF files and extract text from them. The pipeline leverages several powerful libraries including `pdf2image`, `PyPDF2`, `tqdm`, `Pillow`, `pytesseract`, `numpy`, and `opencv-python` to convert PDF pages to images, preprocess the images, and perform OCR to extract text. The extracted text is then saved to a text file for further use.

### Project Structure:
The project consists of the following files and directories:

- `ocr.py`: This is the main script that runs the OCR pipeline. It handles the conversion of PDF pages to images, preprocessing of images, performing OCR, and saving the extracted text to a file.
- `requirements.txt`: This file lists all the Python packages required to run the project. It ensures that all dependencies are installed correctly.
- `output/`: This directory is where the output text files are saved. Each text file corresponds to the text extracted from a PDF file.

### Features:
- **PDF to Image Conversion**: The pipeline uses `pdf2image` to convert each page of the PDF into an image. This is a crucial step as OCR works on images.
- **Image Preprocessing**: The images are preprocessed using OpenCV to enhance the quality and improve OCR accuracy. This includes operations like gray scaling and thresholding
- **Optical Character Recognition**: Tesseract OCR is used to extract text from the preprocessed images. Tesseract is a powerful OCR engine that supports multiple languages and scripts.
- **Text Saving**: The extracted text is saved to a text file in the `output` directory. This allows for easy access and further processing of the text.

### Design Choices:
Several design choices were made during the development of this project to ensure efficiency and accuracy:

1. **Batch Processing**: The pipeline processes images in batches to manage memory usage effectively. This is particularly important when dealing with large PDF files.
2. **Progress Bar**: The `tqdm` library is used to display a progress bar, providing real-time feedback on the processing status. This enhances the user experience by showing the progress of the OCR process.
3. **Memory Management**: After processing each batch of images, the batch is discarded to free up memory. This prevents memory overflow issues and ensures smooth operation. in the beginning i didn't use a generator in the generate_image_batch function because I initially thought that loading images to RAM would be much faster and these images won't take this much RAM but after running the code for the first time i saw huge memory leaks and the script keeps crashing. i realized that i have to revise my design choices and after calculating the ram requirements for the entire pdf file to be processed i concluded that a 300 pages book (with each image being around 24 megabytes) would be about 7.5 gigabytes which is huge even for modern hardware. i then realized that i have to use a generator and process the pdf file in batches and that is the most efficient way of doing it. i thought about saving the extracted image to the hard drive but this introduced tow limitations. first of all this created a bottleneck for the pipeline which is the user storage device (i/o) and even if the user is using a fast SSD that won't be as fast as the RAM and secondly this required the pipeline to iterate over the entire pdf file saving each image to the hard drive and then when the images are extracted entirely then it had to be loaded back to open-cv to preprocess it and then preform OCR on it which is another bottleneck for the pipeline since you are saving images and then loading them back which is inefficient and would require deleting the images after the OCR has finished.
4. **Modular Functions**: The pipeline is divided into modular functions such as `preprocess_image`, `perform_ocr`, and `save_to_txt`. This makes the code more readable, maintainable, and reusable.

### Usage:
To use the OCR pipeline, follow these steps:

1. Install OS dependencies

```bash
sudo apt-get update && sudo apt-get install -y \

    python3-pip \

    poppler-utils \

    tesseract-ocr \

    tesseract-ocr-ara
```

2. **Install Dependencies**: Ensure all required Python packages are installed by running:

```bash
pip install -r requirements.txt
```

3. **Place PDF File**: Place the PDF file you want to process in the project directory.
4. **Run the Script**: Execute the `ocr.py` script by running:

```bash
python ocr.py
```

5. **Enter PDF Name**: When prompted, enter the name of your PDF file (without the `.pdf` extension).
6. **View Results**: The extracted text will be saved in the `output` directory as a `.txt` file.
