<template>
  <div>
    <!-- 웹캠 영상 표시 -->
    <video ref="videoElement" autoplay></video>
    <!-- 얼굴 인식 결과를 그릴 캔버스 -->
    <canvas ref="canvas"></canvas>
    <!-- 인식된 이름을 표시할 영역 -->
    <div ref="nameTag"></div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import * as faceapi from 'face-api.js';

const videoElement = ref<HTMLVideoElement | null>(null);
const canvas = ref<HTMLCanvasElement | null>(null);
const nameTag = ref<HTMLDivElement | null>(null); // 이름 표시 영역

let labeledFaceDescriptors: faceapi.LabeledFaceDescriptors[] = []; //라벨링된 얼굴 정보 배열

onMounted(async () => {
  // 얼굴 인식 모델 로드
  await faceapi.nets.ssdMobilenetv1.loadFromUri('/models'); // ssdMobilenetv1 모델 로드
  await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
  await faceapi.nets.faceRecognitionNet.loadFromUri('/models');

  // 미리 저장된 라벨링된 얼굴 데이터 불러오기
  labeledFaceDescriptors = await loadLabeledImages();

  // 웹캠 스트림 가져오기
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      if (videoElement.value) {
        videoElement.value.srcObject = stream;

        // 웹캠이 로드되면 얼굴 인식 시작
        videoElement.value.onloadedmetadata = () => {
          if (canvas.value) {
            canvas.value.width = videoElement.value.videoWidth;
            canvas.value.height = videoElement.value.videoHeight;
          }
          startFaceDetection(); // 얼굴 인식 시작
        };
      }
    })
    .catch((err) => {
      console.error('웹캠을 불러오지 못했습니다:', err);
    });
});

// 저장된 이미지의 얼굴 특징을 벡터로 추출하고, 라벨을 붙이는 과정
const loadLabeledImages = async () => {
  const labels = ['김이랑', '김정희', '이진우']; // 배열은 인식할 사람들의 이름 목록

  return Promise.all(
    labels.map(async (label) => {
      const imgUrl = `/known/${label}.jpg`; // 이미지 경로에서 이미지 불러오기
      const img = await faceapi.fetchImage(imgUrl); // 불러오는 이미지는 얼굴 인식 모델이 처리할 수 있도록 faceapi.fetchImage()를 사용해 가져옵
      // 얼굴 특징(벡터) 추출
      const detections = await faceapi.detectSingleFace(img) // detectSingleFace 얼굴감지, 얼굴 랜드마크 눈, 코, 입 위치 계산
      .withFaceLandmarks() 
      .withFaceDescriptor(); //얼굴 고유의 특징을 수치화한 디스크립터를 반환, 디스크립터는 벡터 형태로, 얼굴을 숫자로 표현
      if (!detections) {
        throw new Error(`얼굴을 찾을 수 없습니다: ${label}`);
      }

      // 디스크립터(벡터) 콘솔에 출력
      console.log(`${label}의 얼굴 벡터:`, detections.descriptor);

      // 추출한 얼굴 벡터와 해당 이름(label)을 함께 저장
      return new faceapi.LabeledFaceDescriptors(label, [detections.descriptor]);
    })
  );
};

// 얼굴 인식 및 표시 시작
// startFaceDetection 함수내에서 이루어짐. 실시간으로 얼굴을 감지하고 디스크립터(벡터)를 추출
const startFaceDetection = () => {
  if (!canvas.value || !videoElement.value || !nameTag.value) return;

  const context = canvas.value.getContext('2d'); // 캔버스에서 그리기 시작
  if (!context) return;

  setInterval(async () => {
    if (videoElement.value) {
      // 웹캠에서 얼굴 인식
      // 웹캠에서 실시간 얼굴 감지 랜드마크와 디스크립터(벡터) 추출
      const detections = await faceapi.detectAllFaces(videoElement.value)
        .withFaceLandmarks().withFaceDescriptors(); //얼굴 감지 및 랜드마크 추출 

      // 캔버스에 얼굴 인식 결과 그리기
      context.clearRect(0, 0, canvas.value.width, canvas.value.height); //캔버스 초기화
      faceapi.draw.drawDetections(canvas.value, detections); //감지된 얼굴 그리기
      faceapi.draw.drawFaceLandmarks(canvas.value, detections); // 얼굴 랜드마크 그리기

      // FaceMatcher로 얼굴 비교
      // faceapi.FaceMatcher는 추출된 얼굴 디스크립터(백터)를 기준으로 웹캠에서 감지된 얼굴과 미리 저장된 얼굴 벡터 비교
      // labeledFaceDescriptors 미리 저장된 라벨링된 얼굴 데이터 불러오기
      if (detections.length > 0) {
        const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6); // 얼굴 매칭 0.6은 유사도 임계값
        detections.forEach((detection) => {
          const bestMatch = faceMatcher.findBestMatch(detection.descriptor);// 가장 비슷 한 얼굴 찾기

          // 얼굴이 인식되면 이름 표시
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
  }, 100); //100ms마다 인식 실행
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
