import numpy as np
import cv2
import os


class MyVideoCapture:
    """Webカメラから映像を取得し、中心にターゲットマークを描画して表示・保存するクラス。"""

    DELAY: int = 100  # 100 msecのディレイ

    def __init__(self) -> None:
        """Webカメラを初期化する。"""
        self.cap: cv2.VideoCapture = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.captured_img: np.ndarray | None = None

        # ✅ 保存フォルダを事前に作成
        os.makedirs("output_images", exist_ok=True)

    def run(self) -> None:
        """カメラ映像を取得してリアルタイムに加工・表示する。"""
        print("カメラ起動中：'c'でキャプチャ保存、'q'で終了")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("カメラからフレームを取得できませんでした。")
                break

            img: np.ndarray = np.copy(frame)

            rows, cols, _ = img.shape
            center = (int(cols / 2), int(rows / 2))
            img = cv2.circle(img, center, 30, (0, 0, 255), 3)
            img = cv2.circle(img, center, 60, (0, 0, 255), 3)
            img = cv2.line(img, (center[0], center[1] - 80), (center[0], center[1] + 80), (0, 0, 255), 3)
            img = cv2.line(img, (center[0] - 80, center[1]), (center[0] + 80, center[1]), (0, 0, 255), 3)
            img = cv2.flip(img, flipCode=1)

            cv2.imshow('frame', img)
            key = cv2.waitKey(self.DELAY) & 0xFF

            # ✅ 'c'キーでキャプチャして即保存
            if key == ord('c'):
                self.captured_img = frame
                self.write_img()
                print("📸 キャプチャして保存しました。")

            # 'q'キーで終了
            elif key == ord('q'):
                print("終了します。")
                break

    def get_img(self) -> np.ndarray | None:
        """最後にキャプチャされた画像を取得する。"""
        return self.captured_img

    def write_img(self, filepath: str = None) -> None:
        """キャプチャされた画像をファイルに保存する。"""
        if self.captured_img is None:
            raise ValueError("キャプチャ画像が存在しません。run()を実行してから保存してください。")

        if filepath is None:
            filepath = os.path.join("output_images", "camera_capture.png")

        # ✅ 保存フォルダの存在を保証
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        cv2.imwrite(filepath, self.captured_img)
        print(f"保存完了：{filepath}")

    def __del__(self) -> None:
        """終了処理。"""
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = MyVideoCapture()
    app.run()
