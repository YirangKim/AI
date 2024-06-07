# 캠 연결하기
import cv2
import mediapipe as mp

# mediapipe 사용하기
# 손 찾기 관련 기능 불러오기
mp_hands = mp.solutions.hands
# 손 그려주는 기능 불러오기
mp_drawing = mp.solutions.drawing_utils
# 손 찾기 관련 세부 설정
hands = mp_hands.Hands(
    max_num_hands = 1, # 탐지할 최대 손의 갯수
    min_detection_confidence = 0.5, # 표시할 손의 최소 정확도
    min_tracking_confidence = 0.5 # 표시할 관절의 최소 정확도
)

video = cv2.VideoCapture(0)

while video.isOpened() :
    ret, img = video.read()
    img = cv2.flip(img,1)
    # 파이썬이 인식 잘 하도록 BGR → RGB로 변경
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # 손 탐지하기
    result = hands.process(img)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    if not ret :
        break

    # 찾은 손 표시하기
    if result.multi_hand_landmarks is not None :
        print(result.multi_hand_landmarks)

    k = cv2.waitKey(30)
    if k == 49 :
        break
    cv2.imshow('hand', img)

video.release()
cv2.destroyAllWindows()