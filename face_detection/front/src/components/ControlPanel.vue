<template>
  <div :style="controlPanelStyle">
    <button :style="buttonStyle" @click="registerUser">사용자 등록</button>
    <button :style="buttonStyle" @click="resetCamera">카메라 초기화</button>
    <button :style="buttonStyle" @click="captureImage">이미지 캡처</button>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue';

// 컨트롤 패널 스타일 정의
const controlPanelStyle = computed(() => ({
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem', // rem 단위로 유지
}));

// 버튼 스타일 정의
const buttonStyle = computed(() => ({
  padding: '10px 20px', // px 단위로 명확히 정의
  fontSize: '16px', // 폰트 크기 명시
  cursor: 'pointer',
}));

// 버튼 이벤트 핸들러 정의
const registerUser = (): void => {
  alert('사용자가 등록되었습니다.');
};

const resetCamera = (): void => {
  alert('카메라가 초기화되었습니다.');
};

const captureImage = (): void => {
  alert('이미지를 캡처했습니다.');
};
</script>
