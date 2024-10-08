<template>
  <div :style="controlPanelStyle">
    <button :style="buttonStyle" @click="registerUser">사용자 등록</button>
    <button :style="buttonStyle" @click="resetCamera">카메라 초기화</button>
    <button :style="buttonStyle" @click="captureImage">이미지 캡처</button>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'; // ref 대신 computed만 필요합니다

// ControlPanel 레이아웃 스타일 정의
const controlPanelStyle = computed(() => ({
  flex: '0 0 30%',  // HomeView에서 ControlPanel이 30% 차지
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  padding: '1rem',
  backgroundColor: '#f5f5f5',
  gap: '1rem',
  maxWidth: '100%',  // 부모 너비를 넘지 않도록 설정
  maxHeight: '100%', // 부모 높이를 넘지 않도록 설정
  overflow: 'hidden', // 내부 스크롤 방지
}));

// 버튼 스타일 정의
const buttonStyle = computed(() => ({
  padding: '10px 20px',  // 패딩을 줄여 부모 크기를 넘지 않도록 설정
  fontSize: '16px',
  cursor: 'pointer',
  maxWidth: '100%',  // 버튼이 부모의 크기를 넘지 않도록 설정
  maxHeight: '100%', // 버튼이 부모의 높이를 넘지 않도록 설정
}));

// 버튼 클릭 이벤트 핸들러
const registerUser = () => {
  alert('사용자가 등록되었습니다.');
};

const resetCamera = () => {
  alert('카메라가 초기화되었습니다.');
};

const captureImage = () => {
  alert('이미지를 캡처했습니다.');
};
</script>

<style scoped>
/* 추가적인 스타일을 여기에 정의할 수 있습니다. */
</style>
