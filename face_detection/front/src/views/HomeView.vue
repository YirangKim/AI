<template>
  <div :style="homeStyle">
    <CameraView @detectedFace="updateDetectedDescriptor" />
    <InfoPanel :detectedDescriptor="detectedDescriptor" :storedPersons="storedPersons" @updateStoredPersons="updateStoredPersons" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import CameraView from '@/components/CameraView.vue';
import InfoPanel from '@/components/InfoPanel.vue';

const storedPersons = ref<{ id: string; name: string; descriptor: Float32Array }[]>([]);
const detectedDescriptor = ref<Float32Array | null>(null);

// 감지된 얼굴 디스크립터 업데이트 함수
const updateDetectedDescriptor = (data: { descriptor: Float32Array }) => {
  detectedDescriptor.value = data.descriptor;
};

// 저장된 인물 목록 업데이트 함수
const updateStoredPersons = (persons: Array<{ id: string; name: string; descriptor: Float32Array }>) => {
  storedPersons.value = persons;
};

const homeStyle = {
  display: 'flex',
  width: '100%',
  height: '100vh',
};
</script>

<style scoped>
/* 추가적인 스타일 정의 */
</style>
