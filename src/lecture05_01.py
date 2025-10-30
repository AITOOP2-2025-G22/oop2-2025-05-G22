import os
import cv2
import numpy as np
import sys
sys.path.append("/Users/k24085kk/work/oop2/oop2-2025-05-G22/my_module/K21999")

from lecture05_camera_image_capture import MyVideoCapture  # ← 学籍番号に合わせて変更

def lecture05_01():
    # --- カメラキャプチャ ---
    app = MyVideoCapture()
    capture_img = app.run()
    if capture_img is None:
        print("Error: カメラ画像が取得できません。")
        return

    # --- google検索画面画像の読み込み ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    google_path = os.path.join(base_dir, "images", "google.png")
    google_img = cv2.imread(google_path)
    if google_img is None:
        print(f"Error: {google_path} が見つかりません。")
        return

    g_h, g_w, _ = google_img.shape
    c_h, c_w, _ = capture_img.shape

    print(f"google.png size: {google_img.shape}")
    print(f"capture image size: {capture_img.shape}")

    # --- 白色領域のマスク作成 ---
    white_mask = cv2.inRange(google_img, (250, 250, 250), (255, 255, 255))

    # --- カメラ画像をタイル状に展開 ---
    tile_x = int(np.ceil(g_w / c_w))
    tile_y = int(np.ceil(g_h / c_h))
    tiled_img = np.tile(capture_img, (tile_y, tile_x, 1))[:g_h, :g_w]

    # --- 出力画像作成 ---
    mask_3ch = cv2.merge([white_mask, white_mask, white_mask])
    result_img = np.where(mask_3ch == 255, tiled_img, google_img)

    # --- 保存 ---
    output_filename = os.path.join(base_dir, "lecture05_01_K24085.png")  # ← 学籍番号に変更
    cv2.imwrite(output_filename, result_img)
    print(f"出力完了: {output_filename}")

if __name__ == "__main__":
    lecture05_01()
