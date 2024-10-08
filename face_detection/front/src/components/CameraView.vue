<template>
    <div :style="cameraViewStyle">
      <video ref="videoElement" autoplay :style="videoStyle"></video>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { onMounted, ref, computed } from 'vue';
  
  // 카메라 뷰 스타일 설정
  const cameraViewStyle = computed(() => ({
    width: '100%',
    height: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000',
  }));
  
  const videoStyle = computed(() => ({
    width: '100%',
    height: 'auto',
    maxHeight: '400px',
  }));
  
  const videoElement = ref<HTMLVideoElement | null>(null);
  
  onMounted(() => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        if (videoElement.value) {
          videoElement.value.srcObject = stream;
        }
      })
      .catch((err) => {
        console.error('웹캠을 불러오지 못했습니다:', err);
      });
  });
  </script>
  