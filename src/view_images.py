import cv2
import os
import glob

# 이미지 디렉토리 설정
image_dir = "../images"
image_files = sorted(glob.glob(os.path.join(image_dir, "*.jpg")))

if not image_files:
    print("No images found in ./images")
    exit(1)

for img_path in image_files:
    img = cv2.imread(img_path)
    if img is None:
        print(f"Failed to load image: {img_path}")
        continue

    cv2.imshow("Echo-Heal Image Viewer", img)
    key = cv2.waitKey(0)  # 키 입력 대기 (0: 무한)
    if key == 27:  # ESC 키로 종료
        break

cv2.destroyAllWindows()
