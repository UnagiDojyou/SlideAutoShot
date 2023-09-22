import os
import re
import sys
import shutil
from reportlab.pdfgen import canvas
from PIL import Image


def get_float_from_filename(filename):
    # Extract the float number from the filename using regex
    match = re.search(r'Shot_([\d.]+)\.png', filename)
    return float(match.group(1)) if match else None


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py output_file.pdf")
        sys.exit(1)

    output_pdf_file = sys.argv[1]
    output_directory = os.path.splitext(output_pdf_file)[0]

    # Get list of Shot_x.png files in the current directory
    files = [f for f in os.listdir('.') if f.endswith('.png') and 'Shot_' in f]
    if not files:
        print("No Shot_x.png files found in the current directory.")
        sys.exit(1)

    # Sort files by the float x in filename
    files.sort(key=get_float_from_filename)

    # Create a new PDF file
    pdf_canvas = canvas.Canvas(output_pdf_file)

    for file in files:
        print(f'adding {file}')
        image = Image.open(file)
        width, height = image.size

        # Draw each image on a new page in the PDF
        pdf_canvas.setPageSize((width, height))
        pdf_canvas.drawInlineImage(file, 0, 0, width=width, height=height)
        pdf_canvas.showPage()

    pdf_canvas.save()
    print(f"PDF saved to {output_pdf_file}")

    # Create a directory with the same name as the PDF
    os.makedirs(output_directory, exist_ok=True)

    # Move the PNG files to the newly created directory
    for file in files:
        shutil.move(file, os.path.join(output_directory, file))

    print(f"PNG files have been moved to the {output_directory} directory.")


if __name__ == "__main__":
    main()
