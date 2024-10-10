<template>
  <div :style="cameraContainerStyle">
    <!-- 웹캠 영상 표시 -->
    <video ref="videoElement" autoplay></video>
    <!-- 얼굴 인식 결과를 그릴 캔버스 -->
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineEmits, computed } from 'vue';
import * as faceapi from 'face-api.js';

// emits: InfoPanel로 얼굴 인식 데이터를 전달
const emits = defineEmits(['detectedFace']);

// 비디오와 캔버스 ref
const videoElement = ref<HTMLVideoElement | null>(null);
const canvas = ref<HTMLCanvasElement | null>(null);

// 카메라 컨테이너 스타일 (가로 70%)
const cameraContainerStyle = computed(() => ({
  width: '70%',
  position: 'relative',
}));

onMounted(async () => {
  await loadModels();
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      if (videoElement.value) {
        videoElement.value.srcObject = stream;
        videoElement.value.onloadedmetadata = () => {
          if (canvas.value && videoElement.value) {
            canvas.value.width = videoElement.value.videoWidth;
            canvas.value.height = videoElement.value.videoHeight;
          }
          startFaceDetection();
        };
      }
    })
    .catch((err) => console.error('웹캠을 불러오지 못했습니다:', err));
});

// 모델 로드 함수
const loadModels = async () => {
  await faceapi.nets.ssdMobilenetv1.loadFromUri('/models');
  await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
};

// 실시간 얼굴 인식 함수
const startFaceDetection = () => {
  if (!canvas.value || !videoElement.value) return;
  const context = canvas.value.getContext('2d');
  if (!context) return;

  setInterval(async () => {
    if (videoElement.value) {
      const detections = await faceapi.detectAllFaces(videoElement.value)
        .withFaceLandmarks()
        .withFaceDescriptors();

      context.clearRect(0, 0, canvas.value.width, canvas.value.height);
      faceapi.draw.drawDetections(canvas.value, detections);
      faceapi.draw.drawFaceLandmarks(canvas.value, detections);

      if (detections.length > 0) {
        emits('detectedFace', detections[0]); // 감지된 얼굴 데이터를 InfoPanel로 전달
      }
    }
  }, 100);
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
  width: 100%;  /* 부모 크기에 맞춤 */
  height: 100%; /* 부모 크기에 맞춤 */
}
</style>
