# Made by Ungi Dojyou
# unagidojyou.com
import cv2
import time
import numpy as np
import sys
import datetime

def call_diff(url, difftime, maxcount):
    cap = cv2.VideoCapture(url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    prev_frame = None
    dt_old = time.time() - (difftime + 1)
    sum = 0
    count = 0
    small = 255

    try:
        while True:
            ret, frame = cap.read()
            dt_now = time.time()

            if ret and dt_now - dt_old > difftime:
                if prev_frame is not None:
                    diff_ratio = cv2.PSNR(prev_frame, frame)
                    print(diff_ratio)
                    sum += diff_ratio
                    count += 1
                    if diff_ratio < small:
                        small = diff_ratio
                
                # 現在のフレームを次の比較のために保存
                prev_frame = frame.copy()
                dt_old = dt_now
                if count >= maxcount:
                    break

            elif dt_now - dt_old > 5:
                print("Failed to grab frame")
                dt_old = dt_now
                break
    except KeyboardInterrupt:
        pass

    cap.release()
    print("")
    print("Finished!")
    print("Average:",sum/count)
    print("Smallest",small)

def capture_from_url(url, psnr_val ,difftime):
    cap = cv2.VideoCapture(url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    counter = 0
    prev_frame = None
    initial_save = True
    dt_old = time.time() - (difftime + 1)

    try:
        while True:
            ret, frame = cap.read()
            dt_now = time.time()
            #print([dt_now,dt_old])

            if (ret and dt_now - dt_old > difftime) or (ret and initial_save):
                if prev_frame is not None:
                    diff_ratio = cv2.PSNR(prev_frame, frame)
                    print(diff_ratio)
                    # 変化したピクセルの割合がpsnr_val%以上の場合、画像を保存
                    if diff_ratio < psnr_val or initial_save:
                        filename = f"frame_{counter}.png"
                        cv2.imwrite(filename, frame)
                        print(f"Saved frame as {filename}")
                        counter += 1
                        if initial_save:
                            print("First shot done.")
                            initial_save = False

                # 現在のフレームを次の比較のために保存
                prev_frame = frame.copy()
                dt_old = dt_now

            elif dt_now - dt_old > 5:
                print("Failed to grab frame")
                dt_old = dt_now
                break
    except KeyboardInterrupt:
        pass

    cap.release()
    print("Finished!")

if __name__ == "__main__":
    color_similarity_rate = 10
    psnr_val = 20
    difftime = 1
    cal = False
    maxcount = 60
    args = sys.argv[1:]
    #print(len(args))
    if len(args) < 2:
        print("First you must measure PSNR value")
        print("With: python script_name.py <URL> cal (time) (max_count)")
        print("Before you select PSNR value, you can run SlidAutoShot")
        print("Usage: python script_name.py <URL> <PSNR_val> (time)")
        sys.exit(1)
    if len(args) >= 2:
        if args[1] == "cal":
            cal = True
        else:
            psnr_val = float(args[1])
    if len(args) >= 3:
        difftime = float(args[2])
    if len(args) >= 4:
        maxcount = float(args[3])
    url = args[0]

    if cal:
        print(f"conneting to {url}")
        print(f"{difftime} second interval")
        call_diff(url, difftime, maxcount)
    else:
        print(f"{difftime} second interval")
        print(f"PSNR Value {psnr_val}%")
        print(f"conneting to {url}")
        capture_from_url(url, psnr_val ,difftime)
