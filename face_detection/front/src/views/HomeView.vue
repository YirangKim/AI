<template>
  <div :style="homeStyle">
    <CameraView />
    <ControlPanel />
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import CameraView from '@/components/CameraView.vue';
import ControlPanel from '@/components/ControlPanel.vue';

// 홈 화면 레이아웃 스타일 정의
const homeStyle = computed(() => ({
  display: 'flex',
  width: '100%',
  height: '100vh', // 전체 화면 높이 설정
  boxSizing: 'border-box', // 패딩 포함한 크기 계산
  overflow: 'hidden',      // 스크롤을 없앰
}));
</script>

<style scoped>
/* 자식 요소가 부모 요소보다 커지지 않도록 설정 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 자식 요소가 부모 크기보다 커지지 않도록 설정 */
div[style*="display: flex"] > * {
  flex-shrink: 1; /* 자식 요소 축소 */
  max-width: 100%; /* 부모의 100% 너비를 넘지 않도록 설정 */
  max-height: 100%; /* 부모 높이를 넘지 않도록 설정 */
}

/* 기본적으로 body와 html에 적용하여 스크롤을 없앰 */
html, body {
  width: 100%;
  height: 100%;
  overflow: hidden; /* 기본 스크롤 제거 */
}
</style>
