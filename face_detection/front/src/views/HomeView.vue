<template>
  <div :style="homeStyle">
    <!-- CameraView로부터 얼굴 데이터를 받고, InfoPanel에 전달 -->
    <CameraView @detectedFace="updateDetectedDescriptor" />
    <InfoPanel :storedPersons="storedPersons" :detectedDescriptor="detectedDescriptor" @updateStoredPersons="updateStoredPersons" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import CameraView from '@/components/CameraView.vue';
import InfoPanel from '@/components/InfoPanel.vue';

// 저장된 인물 목록과 감지된 디스크립터
const storedPersons = ref<{ id: string; name: string; descriptor: Float32Array }[]>([]);
const detectedDescriptor = ref(null);

// CameraView에서 전달된 얼굴 인식 결과를 업데이트하는 함수
const updateDetectedDescriptor = (newDescriptor) => {
  detectedDescriptor.value = newDescriptor;
};

// InfoPanel에서 저장된 인물 목록을 업데이트하는 함수
const updateStoredPersons = (newPersons) => {
  storedPersons.value = newPersons;
};

// 홈 레이아웃 스타일 정의 (flexbox로 배치)
const homeStyle = {
  display: 'flex',
  width: '100%',
  height: '100vh',
  boxSizing: 'border-box',
};
</script>

<style scoped>
/* 추가적인 스타일 정의 가능 */
</style>
