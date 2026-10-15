from toolbox import update_ui
from toolbox import CatchException

fast_debug = False

from autogen import ConversableAgent
import os
config_list = [{"model": "gpt-3.5-turbo-16k",
                "api_key": os.environ.get("OPENAI_API_KEY", ""),
                "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.xiaoai.plus/v1"),
                "temperature": 0.9
                }]

from toolbox import update_ui
from crazy_functions.auto_gen import update_emo_list
# from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive

from crazy_functions.agent_utils import extract_contents


import cv2
import threading
import time


from keras.utils import img_to_array
import imutils
from keras.models import load_model
import numpy as np
import os

# 设置环境变量
os.environ['XLA_FLAGS'] = '--xla_gpu_cuda_data_dir=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2'
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices=false'

# 参数配置
detection_model_path = 'crazy_functions/emo_agent/face_agent/haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'crazy_functions/emo_agent/face_agent/models/_mini_XCEPTION.102-0.66.hdf5'

# 加载模型
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# 面部识别模型的情绪列表
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

def process_image(image):
    # 对采集的图像进行情绪识别
    # # 保存处理后的图像
    # cv2.imwrite('gpt_log/processed_image.jpg', gray_image)
    # print("图像已处理并保存为 processed_image.jpg")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    canvas = np.zeros((250, 300, 3), dtype="uint8")
    frameClone = image.copy()
    if len(faces) > 0:
        faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        preds = emotion_classifier.predict(roi)[0]
        emo_id = preds.argmax()
        update_emo_list(emo_id)




def capture_images():
    cap = cv2.VideoCapture(0)  # 打开默认摄像头
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    try:
        # 立即拍照并处理图像
        ret, frame = cap.read()  # 捕获一帧
        if ret:
            process_image(frame)
        else:
            print("无法读取摄像头数据")

        while True:
            # 等待30秒
            time.sleep(5)

            # 每隔30秒拍照一次并处理图像
            ret, frame = cap.read()  # 捕获一帧
            if not ret:
                print("无法读取摄像头数据")
                break

            process_image(frame)
    finally:
        cap.release()  # 释放摄像头资源
        cv2.destroyAllWindows()

def start_camera_thread():
    # 创建并启动一个线程来运行摄像头任务
    camera_thread = threading.Thread(target=capture_images, daemon=True)
    camera_thread.start()


import time
@CatchException
def 面部情绪识别助理(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    import glob, os

    chatbot.append([
        "摄像头权限已开启",
        None])
    yield from update_ui(chatbot=chatbot, history=history)

    time.sleep(1)

    chatbot.append([
        "面部情绪识别助理已生成",
        None])
    yield from update_ui(chatbot=chatbot, history=history)

    chatbot.append([
        "注意：该智能体用于后端与其他智能体交互，实际不出现在用户界面",
        None])
    yield from update_ui(chatbot=chatbot, history=history)

    # time.sleep(1)
    # chatbot.append([
    #     "面部情绪识别模型载入中，请稍后",
    #     None])
    # yield from update_ui(chatbot=chatbot, history=history)
    #
    # time.sleep(5)
    # chatbot.append([
    #     "检测到当前面部情绪：中性",
    #     None])
    # yield from update_ui(chatbot=chatbot, history=history)
    #
    #
    # time.sleep(3)
    # chatbot.append([
    #     "检测到当前面部情绪：沮丧",
    #     None])
    # yield from update_ui(chatbot=chatbot, history=history)
    #
    #
    # time.sleep(2)
    # chatbot.append([
    #     "检测到当前面部情绪：中性",
    #     None])
    # yield from update_ui(chatbot=chatbot, history=history)


    # 这里开摄像头权限，系统每隔5秒拍照存照片，识别情绪
    # 启动摄像头线程
    start_camera_thread()




