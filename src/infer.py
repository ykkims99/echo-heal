
import onnxruntime as ort
import cv2
import numpy as np
import argparse
import time
import matplotlib.pyplot as plt

def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (224, 224))
    x = img.transpose(2, 0, 1).astype(np.float32) / 255.0
    x = np.expand_dims(x, axis=0)
    return x, img

def postprocess_result(probability, recovery_days):
    print(f"Healing Probability (P_heal): {probability:.2f}")
    print(f"Estimated Recovery Time (T̂_recover): {recovery_days:.1f} days")

def run_inference(input_path, output_path):
    x, original_img = preprocess_image(input_path)

    sess = ort.InferenceSession('models/echo_heal_v1.onnx')
    input_name = sess.get_inputs()[0].name

    start_time = time.time()
    outputs = sess.run(None, {input_name: x})
    latency = (time.time() - start_time) * 1000  # ms

    p_heal = outputs[0][0][0]   # assuming shape (1,1)
    t_recover = outputs[1][0][0]  # assuming shape (1,1)

    postprocess_result(p_heal, t_recover)
    print(f"Inference Time: {latency:.1f} ms")

    # Simulated Grad-CAM (replace with real CAM if supported)
    cam_overlay = cv2.addWeighted(original_img, 0.6, np.full_like(original_img, [0, 0, 255]), 0.4, 0)
    cv2.imwrite(output_path, cam_overlay)

    plt.imshow(cv2.cvtColor(cam_overlay, cv2.COLOR_BGR2RGB))
    plt.title("Simulated Grad-CAM")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()

    run_inference(args.input, args.output)
