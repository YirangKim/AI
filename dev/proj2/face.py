# Step 1 모듈 가져오기
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

# Step 2 추론기 만듬
app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640)) #prepare 얼굴분석기

# Step 3 웹캠 연결 및 캡쳐
def capture_face_from_webcam(output_path="webcam_capture.jpg"):
    cap = cv2.VideoCapture(0)  # 0번 카메라를 엽니다.
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return None, None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("캡쳐 실패")
            break

        # 얼굴 검출
        faces = app.get(frame)

        # 얼굴이 검출되면 사각형으로 표시
        for face in faces:
            box = face.bbox.astype(int)
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        # 얼굴이 검출된 프레임을 저장하고 반환
        if faces:
            cv2.imwrite(output_path, frame)
            cap.release()
            return frame, faces

    cap.release()
    return None, None

img, faces1 = capture_face_from_webcam()
if img is None or faces1 is None:
    print("얼굴 캡쳐 실패")
    exit()

# Step 4 다른 이미지 가져오기
img2 = cv2.imread('img1.png', cv2.IMREAD_COLOR)

# Step 5 추론
faces2 = app.get(img2)

# Step 6 후처리 출력
rimg = app.draw_on(img, faces1) # 이미지 위에 얼굴 검출 결과 그리기
cv2.imwrite("./boy_output.jpg", rimg) # 결과 이미지를 파일로 저장

print(len(faces1))
print(faces1[0].embedding)

# then print all-to-all face similarity
feat1 = np.array(faces1[0].normed_embedding, dtype=np.float32) #normed_embedding: 얼굴의 고유한 특징을 나타내는 벡터
feat2 = np.array(faces2[0].normed_embedding, dtype=np.float32)

sims = np.dot(feat1, feat2.T) #np.dot: 두 벡터의 내적을 계산하여 유사도를 측정
print(sims)

# 얼굴 유사도 판단 및 출력
threshold = 0.5 # 유사도 임계값 설정 (0.5는 예시 값이며 조정 가능)

if sims > threshold:
    print("얼굴이 유사합니다")
else:
    print("동일 인물이 아닙니다")