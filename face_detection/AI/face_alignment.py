# face_alignment.py
# 얼굴 정렬 기능 정의

import os
import cv2
import dlib
import numpy as np

# 현재 파일의 위치를 기준으로 모델 파일 경로 지정
current_directory = os.path.dirname(__file__)
model_path = os.path.join(current_directory, "shape_predictor_68_face_landmarks.dat")
# Dlib 라이브러리에서 사용하는 사전 학습된 얼굴 랜드마크 모델
# 이 모델은 이미지를 입력으로 받아 얼굴에서 특정한 68개의 주요 랜드마크 포인트(눈, 코, 입, 얼굴 윤곽 등)를 검출하는 역할

# dlib의 얼굴 탐지기와 랜드마크 예측기 로드
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(model_path)  # 이동된 파일 경로를 지정하여 68점 랜드마크 모델 로드

# 얼굴 정렬 함수
def face_alignment(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {image_path}")

    # 얼굴 검출
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        return None  # 얼굴이 검출되지 않으면 None 반환

    # 첫 번째 얼굴에 대해서만 정렬 수행
    face = faces[0]
    landmarks = predictor(gray, face)
    landmarks_points = []

    # 랜드마크 좌표 추출 및 출력
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        landmarks_points.append((x, y))
        
        # 각 포인트 좌표 출력
        print(f"Point {n + 1}: ({x}, {y})")
        
        # 이미지에 포인트 그리기 (검은색 점)
        cv2.circle(image, (x, y), 2, (0, 0, 0), -1)  # 반지름 2의 검은색 원으로 표시

    # 랜드마크 좌표를 NumPy 배열로 변환합니다.
    landmarks_points = np.array(landmarks_points, dtype='int')

    # 두 눈을 기준으로 얼굴 정렬
    left_eye_pts = landmarks_points[36:42]
    right_eye_pts = landmarks_points[42:48]

    left_eye_center = np.mean(left_eye_pts, axis=0)
    right_eye_center = np.mean(right_eye_pts, axis=0)

    # 두 눈의 각도 계산 및 회전
    dY = right_eye_center[1] - left_eye_center[1]
    dX = right_eye_center[0] - left_eye_center[0]
    angle = np.degrees(np.arctan2(dY, dX))

    # 두 눈 중심점 계산
    eyes_center = (int((left_eye_center[0] + right_eye_center[0]) / 2),
                   int((left_eye_center[1] + right_eye_center[1]) / 2))

    # 회전 행렬 계산 및 이미지 회전
    rotation_matrix = cv2.getRotationMatrix2D(eyes_center, angle, scale=1)
    aligned_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]), flags=cv2.INTER_CUBIC)

    # 정렬된 이미지 파일 저장
    output_path = "aligned_" + os.path.basename(image_path)
    cv2.imwrite(output_path, aligned_image)
    

    # 68개 포인트가 표시된 원본 이미지도 저장합니다.
    points_output_path = "landmarks_" + os.path.basename(image_path)
    cv2.imwrite(points_output_path, image)

    # 결과 이미지를 표시하여 확인할 수 있습니다.
    cv2.imshow("Landmarks", image)
    cv2.imshow("Aligned Face", aligned_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return output_path

