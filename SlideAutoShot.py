# Made by Ungi Dojyou
# unagidojyou.com
import cv2
import time
import numpy as np
import sys


def calculate_pixel_difference(img1, img2, color_similarity_rate):
    """ 2つの画像間のピクセルごとの色の差を計算し、変化したピクセルの割合を返す """
    # 色の差を計算
    diff = cv2.absdiff(img1, img2)

    # color_similarity_rate%以上の色の差があるピクセルを判定
    threshold = color_similarity_rate * 255 / 100  # color_similarity_rate% of 255
    significant_diff = np.greater(diff, threshold)

    # 3チャネルのブール値を合算して1チャネルに変換
    significant_diff_single_channel = np.sum(significant_diff, axis=2) > 0

    # 変化したピクセルの割合を計算
    total_pixels = img1.shape[0] * img1.shape[1]  # 縦 x 横
    changed_pixels = np.sum(significant_diff_single_channel)
    ratio = changed_pixels / total_pixels
    # print(ratio)

    return ratio


def capture_from_url(url, color_similarity_rate, pixel_rate):
    cap = cv2.VideoCapture(url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    counter = 0
    prev_frame = None
    initial_save = True

    try:
        while True:
            ret, frame = cap.read()

            if ret:
                if prev_frame is not None:
                    diff_ratio = calculate_pixel_difference(
                        prev_frame, frame, color_similarity_rate)
                    # 変化したピクセルの割合がpixel_rate%以上の場合、画像を保存
                    if diff_ratio > (pixel_rate / 100) or initial_save:
                        filename = f"frame_{counter}.png"
                        cv2.imwrite(filename, frame)
                        print(f"Saved frame as {filename}")
                        counter += 1
                        initial_save = False

                # 現在のフレームを次の比較のために保存
                prev_frame = frame.copy()

                time.sleep(1)
            else:
                print("Failed to grab frame")
                break
    except KeyboardInterrupt:
        pass

    cap.release()
    print("Finished!")


if __name__ == "__main__":
    color_similarity_rate = 10
    pixel_rate = 20
    args = sys.argv[1:]
    print(len(args))
    if len(args) < 1:
        print("Usage: python script_name.py <URL> (Color similarity %) (Pixel %)")
        sys.exit(1)
    elif len(args) == 2:
        color_similarity_rate = float(args[1])
    if len(args) == 3:
        color_similarity_rate = float(args[1])
        pixel_rate = float(args[2])
    url = args[0]

    print(f"Color similarity rate {color_similarity_rate}%")
    print(f"Pixel rate {pixel_rate}%")
    print(f"conneting to {url}")
    capture_from_url(url, color_similarity_rate, pixel_rate)
