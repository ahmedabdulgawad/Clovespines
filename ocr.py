from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from tqdm import tqdm
from PIL import Image
import pytesseract
import numpy as np
import cv2
import os


"""Initialize models and configurations"""
def initialize_models():
    # Prompt user for input PDF file name
    try:
        pdf_name = input("Please enter your PDF file name (don't include .pdf!): ")
        if not os.path.exists(f"{pdf_name}.pdf"):
            raise FileNotFoundError(f"File {pdf_name}.pdf does not exist")
        pdf_path = os.path.join(os.getcwd(), f"{pdf_name}.pdf")
    except Exception as e:
        print(f"Error: {e}")

    # Create the output directory if it doesn't exist
    output_dir_name = "output"
    os.makedirs(output_dir_name, exist_ok=True)
    output_path = os.path.join(os.getcwd(), output_dir_name)

    # PDF total number of pages and batch size
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"Total pages in the PDF: {total_pages}")
    batch_size = 10 # Adjust batch size according to memory constraints

    # load tesseract model
    pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
    return pdf_path, output_path, pdf_name, total_pages, batch_size


"""Preprocessing"""
def generate_image_batches(pdf_path, batch_size, total_pages):
    try:
        """
        Generator that yields batches of images from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file.
            batch_size (int): Number of pages to process per batch.
            total_pages (int): Total number of pages in the PDF.

        Yields:
            List[Image]: List of PIL Image objects for the current batch.
        """
        start_page = 1  # Start from the first page
        total_pages = 20  # For testing purposes delete this line
        while start_page <= total_pages:
            # Determine the range of pages for the current batch
            end_page = min(start_page + batch_size - 1, total_pages)

            # Convert the current batch of pages to images
            images = convert_from_path(
                pdf_path,
                first_page=start_page,
                last_page=end_page,
                fmt="tiff",
                dpi=300,
                thread_count=4,
            )

            # Yield the batch of images
            yield images

            # Move to the next batch
            start_page = end_page + 1

    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")

# Preprocess the images
def preprocess_image(page):
    try:
        # Convert image to numpy array
        image_array = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        # Convert image to grayscale
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # Apply OTSU thresholding
        _, thresholded = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # Convert the NumPy array to a PIL Image
        pil_image = Image.fromarray(thresholded)
        return pil_image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


"""preform OCR"""
def perform_ocr(pre_img):
    # Configuration for tesseract
    custom_config = '--psm 6 -l ara' # Page segmentation mode 6(best for books), Arabic language
    text = pytesseract.image_to_string(pre_img, config=custom_config)
    return text


"""save output"""
def save_to_txt(all_text, txt_path):
    with open(txt_path, "w", encoding="utf-8") as file:
        for page_number, text in enumerate(all_text, start=1):
            file.write(f"Page {page_number}\n{text}\n\n")


"""main workflow"""
def main():
    # Initialize models and configurations
    pdf_path, output_path, pdf_name, total_pages, batch_size = initialize_models()

    # Initialize document content
    all_text = []
    txt_path = os.path.join(output_path, f"{pdf_name}.txt")

    # Add progress bar for total pages
    with tqdm(total=total_pages, desc="Processing pages") as pbar:
        # Process PDF in batches and collect OCR results
        for image_batch in generate_image_batches(pdf_path, batch_size, total_pages):
            # Perform OCR on the current batch
            for image in image_batch:
                # Preprocess the image
                preprocessed_image = preprocess_image(image)

                # Perform OCR on the preprocessed image and save the text
                text = perform_ocr(preprocessed_image)

                # Append the text to the list
                all_text.append(text)
                pbar.update(1)  # Update progress after each page

            # Discard image batch to free memory
            del image_batch

    # Save the OCR results to a text file
    save_to_txt(all_text, txt_path)
    print(f"OCR process completed. Text saved to {txt_path}")

# Run the pipeline
if __name__ == "__main__":
    main()
