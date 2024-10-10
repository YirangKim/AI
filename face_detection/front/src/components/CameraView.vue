<template>
  <div :style="cameraStyle">
    <!-- 웹캠 영상 표시 -->
    <video ref="videoElement" autoplay></video>
    <!-- 얼굴 인식 결과를 그릴 캔버스 -->
    <canvas ref="canvas"></canvas>
    <!-- 인식된 이름을 표시할 영역 -->
    <div ref="nameTag"></div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineEmits } from 'vue';
import * as faceapi from 'face-api.js';

const emits = defineEmits(['detectedFace']);
const videoElement = ref<HTMLVideoElement | null>(null);
const canvas = ref<HTMLCanvasElement | null>(null);
const nameTag = ref<HTMLDivElement | null>(null);

onMounted(async () => {
  await loadModels();  // 얼굴 인식 모델 로드

  // 웹캠 스트림 가져오기
  navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
    if (videoElement.value) {
      videoElement.value.srcObject = stream;
      videoElement.value.onloadedmetadata = () => {
        if (canvas.value && videoElement.value) {
          canvas.value.width = videoElement.value.videoWidth;
          canvas.value.height = videoElement.value.videoHeight;
          startFaceDetection(); // 얼굴 인식 시작
        }
      };
    }
  }).catch((err) => console.error('웹캠을 불러오지 못했습니다:', err));
});

// 실시간 얼굴 인식 함수
const startFaceDetection = () => {
  if (!canvas.value || !videoElement.value || !nameTag.value) return;
  const context = canvas.value.getContext('2d');
  if (!context) return;

  setInterval(async () => {
    if (videoElement.value) {
      const detections = await faceapi.detectAllFaces(videoElement.value)
        .withFaceLandmarks()
        .withFaceDescriptors();

      context.clearRect(0, 0, canvas.value.width, canvas.value.height); // 캔버스 초기화
      faceapi.draw.drawDetections(canvas.value, detections);  // 얼굴 그리기
      faceapi.draw.drawFaceLandmarks(canvas.value, detections);  // 얼굴 랜드마크 그리기

      if (detections.length > 0) {
        const detection = detections[0];  // 첫 번째 감지된 얼굴만 처리
        emits('detectedFace', { descriptor: detection.descriptor });  // 감지된 디스크립터를 InfoPanel로 전달
        nameTag.value!.innerText = '얼굴 감지됨!';
      } else {
        nameTag.value!.innerText = '얼굴을 감지하지 못했습니다.';
      }
    }
  }, 100);  // 100ms마다 인식 실행
};

// 얼굴 인식 모델 로드 함수
const loadModels = async () => {
  await faceapi.nets.ssdMobilenetv1.loadFromUri('/models');
  await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
};

// 카메라 스타일 정의 (70% 너비 설정)
const cameraStyle = {
  width: '70%',  // 가로 70% 설정
  padding: '10px',
  position: 'relative'
};
</script>

<style scoped>
video {
  width: 100%;
  max-height: 100%;
}

canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

div {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(255, 255, 255, 0.7);
  padding: 10px;
  border-radius: 5px;
}
</style>
