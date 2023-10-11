import os
import re
import sys
import shutil
from reportlab.pdfgen import canvas
from PIL import Image
from collections import Counter


def get_float_from_filename(filename):
    # Extract the float number from the filename using regex
    match = re.search(r'Shot_([\d.]+)\.png', filename)
    return float(match.group(1)) if match else None


def get_most_common_resolution():
    # カレントディレクトリ内のファイルを取得
    files = os.listdir()

    # Shot_x.png (xはfloat) のパターンをコンパイル
    pattern = re.compile(r'Shot_([\d.]+)\.png')

    resolutions = []

    # 各ファイルに対して
    for file in files:

        if pattern.match(file):
            # print(file)
            with Image.open(file) as img:
                resolutions.append(img.size)
                # print(img.size)

    # 最も一般的な解像度を取得
    if resolutions:
        most_common_resolution = Counter(resolutions).most_common(1)[0][0]
        return most_common_resolution
    else:
        return None


def change_resolution(target_width):
    # カレントディレクトリ内のファイルを取得
    files = os.listdir()

    # Shot_x.png (xはfloat) のパターンをコンパイル
    pattern = re.compile(r'Shot_([\d.]+)\.png')

    # 各ファイルに対して
    for file in files:
        if pattern.match(file):
            with Image.open(file) as img:
                # 与えられた横方向の解像度と異なる場合
                if img.width != target_width:
                    # 縦横比を維持しつつリサイズ
                    new_height = int(target_width * (img.height / img.width))
                    img_resized = img.resize(
                        (target_width, new_height), Image.LANCZOS)

                    # ファイルを上書き保存
                    img_resized.save(file)
                    print(f"Resize {file}")


def makepdf(output_pdf_file):

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
    if len(sys.argv) < 2:
        print("Usage: python script.py output_file.pdf")
        sys.exit(1)
    output_pdf_file = sys.argv[1]

    resolution = get_most_common_resolution()
    change_resolution(resolution[0])
    makepdf(output_pdf_file)
