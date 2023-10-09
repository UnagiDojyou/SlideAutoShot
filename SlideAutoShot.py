# Made by Ungi Dojyou
# unagidojyou.com
import cv2
import time
import numpy as np
import sys
import datetime
import glob
import re
import threading
import keyboard
import platform
import os

save_flag = False
quit_flag = False


# ファイルの最大値を見つける
def find_max_x():
    # カレントディレクトリの Shot_x.png ファイルを列挙
    files = glob.glob('Shot_*.png')

    max_x = -1  # 初期値。まだファイルを見つけていないので-1を設定

    for file in files:
        # 正規表現で x の値を抜き出す
        match = re.match(r'Shot_(\d+).png', file)
        if match:
            x = int(match.group(1))  # グループ1には x の値が入っている
            if x > max_x:
                max_x = x  # より大きな x の値を見つけたら更新

    return max_x + 1  # 最大の x の値を返す。ファイルが一つも無い場合は0


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


def check_keyboard():
    system_name = platform.system()

    if system_name == "Linux" or system_name == "Darwin":
        return os.geteuid() == 0
    elif system_name == "Windows":
        return True
    else:
        return False


# キーを監視(sが押されたら撮る、qが押されたら終了する)
def check_for_s_key():
    global save_flag
    global quit_flag
    print("Press 's' to save a frame or 'q' to quit.")
    while True:
        if keyboard.is_pressed('s'):
            save_flag = True
            time.sleep(0.5)  # 過剰な反応を避けるための遅延
        elif keyboard.is_pressed('q'):
            quit_flag = True
            break
        time.sleep(0.01)


def capture_from_url(url, color_similarity_rate, pixel_rate, difftime):
    cap = cv2.VideoCapture(url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    counter = find_max_x()
    prev_frame = None
    initial_save = True
    dt_old = time.time() - 6.0
    global save_flag
    global quit_flag
    try:
        while True:
            ret, frame = cap.read()
            dt_now = time.time()

            if (ret and dt_now - dt_old > difftime) or (ret and initial_save) or save_flag:
                if prev_frame is not None:
                    diff_ratio = calculate_pixel_difference(
                        prev_frame, frame, color_similarity_rate)
                    # 変化したピクセルの割合がpixel_rate%以上の場合、画像を保存
                    if diff_ratio > (pixel_rate / 100) or initial_save or save_flag:
                        filename = f"Shot_{counter}.png"
                        cv2.imwrite(filename, frame)
                        print(f"Saved frame as {filename}")
                        counter += 1
                        if initial_save:
                            print("First shot done.")
                            initial_save = False
                        if save_flag:
                            print("Saved due to 's' key input.")
                            save_flag = False

                # 現在のフレームを次の比較のために保存
                prev_frame = frame.copy()
                dt_old = dt_now

            elif dt_now - dt_old > 5:
                print("Failed to grab frame")
                dt_old = dt_now
                break
            elif quit_flag:
                print("'q' key input")
                break
    except KeyboardInterrupt:
        pass

    cap.release()
    print("Finished!")


if __name__ == "__main__":
    color_similarity_rate = 10
    pixel_rate = 10
    difftime = 1
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: python script_name.py <URL> (time) (Color similarity %) (Pixel %)")
        sys.exit(1)
    elif len(args) == 2:
        difftime = float(args[1])
    if len(args) == 3:
        difftime = float(args[1])
        color_similarity_rate = float(args[2])
    if len(args) == 4:
        difftime = float(args[1])
        color_similarity_rate = float(args[2])
        pixel_rate = float(args[3])
    url = args[0]

    print(f"Color similarity rate {color_similarity_rate}%")
    print(f"Pixel rate {pixel_rate}%")
    print(f"conneting to {url}")
    if check_keyboard():
        input_thread = threading.Thread(target=check_for_s_key)
        input_thread.start()
    else:
        print("if you want to use keyboard to shot with 's',you have to run with sudo.")
    capture_from_url(url, color_similarity_rate, pixel_rate, difftime)
