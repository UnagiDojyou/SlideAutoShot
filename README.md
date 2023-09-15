# SlideAutoShot
IPカメラでスライドが表示されている画面などを写し、画面が変わったら自動的に写真を撮るスクリプトです。
1秒ごとに画像を取得し、一枚前の画像と色がcolor_similarity_rate㌫以上変わったピクセルが全体のpixel_rate㌫存在した場合、画像を保存します。

# 使い方
```
SlideAutoShot.py IPカメラのURL color_similarity_rate pixel_rate
```
color_similarity_rateとpixel_rateはオプション(未指定で10と20)