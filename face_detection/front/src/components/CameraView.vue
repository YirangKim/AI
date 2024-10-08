<template>
  <div>
    <video ref="videoElement" autoplay></video>
    <canvas ref="canvas"></canvas>
    <div ref="nameTag"></div> <!-- 인식된 이름을 표시할 영역 -->
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import * as faceapi from 'face-api.js';

const videoElement = ref<HTMLVideoElement | null>(null);
const canvas = ref<HTMLCanvasElement | null>(null);
const nameTag = ref<HTMLDivElement | null>(null); // 이름 표시 영역

let labeledFaceDescriptors: faceapi.LabeledFaceDescriptors[] = [];

onMounted(async () => {
  // 얼굴 인식 모델 로드
  await faceapi.nets.ssdMobilenetv1.loadFromUri('/models'); // ssdMobilenetv1 모델 로드
  await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('/models');

  // 사전 저장된 얼굴 데이터 로드
  labeledFaceDescriptors = await loadLabeledImages();

  // 웹캠 스트림 가져오기
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      if (videoElement.value) {
        videoElement.value.srcObject = stream;

        videoElement.value.onloadedmetadata = () => {
          if (canvas.value) {
            canvas.value.width = videoElement.value.videoWidth;
            canvas.value.height = videoElement.value.videoHeight;
          }
          // 얼굴 인식 시작
          startFaceDetection();
        };
      }
    })
    .catch((err) => {
      console.error('웹캠을 불러오지 못했습니다:', err);
    });
});

// 사전에 저장된 이미지의 얼굴 특징을 벡터화하여 라벨링
const loadLabeledImages = async () => {
  const labels = ['김이랑', '김정희', '이진우']; // 라벨(이름)

  return Promise.all(
    labels.map(async (label) => {
      // 해당 라벨에 해당하는 이미지를 로드
      const imgUrl = `/known/${label}.jpg`; // 예시: 김이랑.jpg, 김정희.jpg 등
      const img = await faceapi.fetchImage(imgUrl);

      // 얼굴 특징(벡터) 추출
      const detections = await faceapi.detectSingleFace(img).withFaceLandmarks().withFaceDescriptor();
      if (!detections) {
        throw new Error(`얼굴을 찾을 수 없습니다: ${label}`);
      }

      // 추출한 얼굴 벡터와 해당 이름(label)을 함께 저장
      return new faceapi.LabeledFaceDescriptors(label, [detections.descriptor]);
    })
  );
};

// 얼굴 인식 시작
const startFaceDetection = () => {
  if (!canvas.value || !videoElement.value || !nameTag.value) return;

  const context = canvas.value.getContext('2d');
  if (!context) return;

  setInterval(async () => {
    if (videoElement.value) {
      // 웹캠에서 얼굴 감지 및 랜드마크, 디스크립터 추출
      const detections = await faceapi.detectAllFaces(videoElement.value)
        .withFaceLandmarks()
        .withFaceDescriptors();

      // 캔버스에 얼굴 인식 결과 그리기
      context.clearRect(0, 0, canvas.value.width, canvas.value.height);
      faceapi.draw.drawDetections(canvas.value, detections);
      faceapi.draw.drawFaceLandmarks(canvas.value, detections);

      if (detections.length > 0) {
        const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6); // 0.6은 유사도 임계값
        detections.forEach((detection) => {
          const bestMatch = faceMatcher.findBestMatch(detection.descriptor);

          if (bestMatch.label !== 'unknown') {
            nameTag.value!.innerText = `인식된 사람: ${bestMatch.label}`;
          } else {
            nameTag.value!.innerText = '알 수 없는 사람';
          }
        });
      } else {
        nameTag.value!.innerText = ''; // 얼굴이 없을 때는 이름을 지움
      }
    }
  }, 100);
};
</script>

<style scoped>
video {
  width: 100%; /* 비디오 너비 설정 */
  max-height: 100%; /* 최대 높이 설정 */
}

canvas {
  position: absolute; /* 캔버스를 비디오 위에 겹치게 설정 */
  top: 0;
  left: 0;
}

div {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(255, 255, 255, 0.7); /* 반투명 배경 */
  padding: 10px;
  border-radius: 5px;
}
</style>
