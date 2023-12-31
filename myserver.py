from flask import Flask, send_file
import os
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)


@app.route("/")
def index():
    img_dir = '.'
    images = [f for f in os.listdir(img_dir) if f.startswith(
        'Shot_') and f.endswith('.png')]

    # floatでソート
    images.sort(key=lambda x: float(x.split('_')[1].split('.png')[0]))

    img_tags = []
    for img in images:
        thumb_io = BytesIO()
        img_path = os.path.join(img_dir, img)
        image = Image.open(img_path)
        image.thumbnail((300, 300))
        image.save(thumb_io, format='PNG')
        thumb_io.seek(0)
        img_tags.append(
            f'<div style=\"display:inline-block; text-align:center; margin:10px;\">'
            f'<a href=\"{img_path}\"><img src=\"data:image/png;base64,{base64.b64encode(thumb_io.read()).decode("utf-8")}\"></a>'
            f'<br><span>{img}</span></div>'
        )

    footer = '<div style="margin-top: 20px; text-align: center;"><a href= https://github.com/UnagiDojyou/SlideAutoShot target="_blank" >SlideAutoShot</a> made by <a href= https://unagidojyou.com target="_blank" >UnagiDojyou</a></div>'

    return f"<!doctype html><html><body>{''.join(img_tags)}{footer}</body></html>"


@app.route('/<img_name>')
def serve_image(img_name):
    return send_file(img_name)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
