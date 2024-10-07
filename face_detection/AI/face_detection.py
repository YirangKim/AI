# face_detection.py

import os
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import time

# 환경 변수 설정: AVFoundation 권한 요청을 건너뛰도록 설정 (MacOS 용)
os.environ["OPENCV_AVFOUNDATION_SKIP_AUTH"] = "1"

# Step 2 추론기 설정
app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))  # 얼굴 분석기 준비

# 전역 변수로 종료 플래그 추가
exit_flag = False

# Step 3 웹캠 연결 및 얼굴 검출 함수
def capture_face_from_webcam(output_path_template="webcam_capture{}.jpg"):
    global exit_flag
    cap = cv2.VideoCapture(0)  # 0번 카메라를 엽니다.

    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return

    capture_index = 0

    while not exit_flag:
        ret, frame = cap.read()
        if not ret:
            print("프레임 읽기 실패")
            break

        # 얼굴 검출
        faces = app.get(frame)

        # 얼굴이 검출되면 사각형으로 표시
        for face in faces:
            box = face.bbox.astype(int)
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        # 얼굴이 검출된 프레임을 파일로 저장 (필요에 따라 주석 처리 가능)
        output_path = output_path_template.format(capture_index)
        cv2.imwrite(output_path, frame)
        print(f"캡쳐 저장됨: {output_path}")
        capture_index += 1

        # 짧은 지연 추가
        time.sleep(0.1)

    cap.release()
    # cv2.destroyAllWindows()는 GUI 창을 사용하는 경우에만 필요하므로 제거

# 종료 신호를 받기 위한 함수..
def set_exit_flag(value: bool):
    global exit_flag
    exit_flag = value
