<template>
  <div>
    <video ref="videoElement" autoplay></video>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import * as faceapi from 'face-api.js';

const videoElement = ref<HTMLVideoElement | null>(null);
const canvas = ref<HTMLCanvasElement | null>(null);

onMounted(async () => {
  // 얼굴 인식 모델 로드 (tinyFaceDetector 사용 시)
  await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
  await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('/models');

  // 웹캠 스트림 가져오기
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      if (videoElement.value) {
        videoElement.value.srcObject = stream;

        // 비디오 메타데이터가 로드되었을 때 비디오 크기 확인 및 얼굴 감지 시작
        videoElement.value.onloadedmetadata = () => {
          console.log('Video Width:', videoElement.value.videoWidth);
          console.log('Video Height:', videoElement.value.videoHeight);

          // canvas의 크기를 비디오 크기로 설정
          if (canvas.value) {
            canvas.value.width = videoElement.value.videoWidth;
            canvas.value.height = videoElement.value.videoHeight;
          }

          // 얼굴 감지 시작
          startFaceDetection();
        };
      }
    })
    .catch((err) => {
      console.error('웹캠을 불러오지 못했습니다:', err);
    });
});

// 얼굴 감지 시작
const startFaceDetection = () => {
  // canvas와 videoElement의 null 체크
  if (!canvas.value || !videoElement.value) return;

  const context = canvas.value.getContext('2d');
  if (!context) return;

  setInterval(async () => {
    if (videoElement.value) {
      // tinyFaceDetector를 사용할 경우 옵션 추가
      const detections = await faceapi.detectAllFaces(videoElement.value, new faceapi.TinyFaceDetectorOptions())
        .withFaceLandmarks();

      // 이전 프레임 지우기 및 감지 박스 그리기
      if (context) {
        context.clearRect(0, 0, canvas.value.width, canvas.value.height);
        faceapi.draw.drawDetections(canvas.value, detections);
        faceapi.draw.drawFaceLandmarks(canvas.value, detections);
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
</style>
