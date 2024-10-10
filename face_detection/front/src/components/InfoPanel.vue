<template>
  <div :style="infoPanelStyle">
    <h3>인물 정보 저장</h3>
    <input v-model="inputId" placeholder="ID 입력" />
    <input v-model="inputName" placeholder="이름 입력" />
    <button @click="saveDetectedPerson">저장</button>

    <h3>저장된 인물 목록:</h3>
    <ul>
      <li v-for="person in storedPersons" :key="person.id">
        {{ person.id }} - {{ person.name }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, defineEmits, defineProps } from 'vue';

// InfoPanel은 CameraView로부터 감지된 얼굴 데이터를 받음
const props = defineProps({
  detectedDescriptor: Object,  // CameraView에서 전달된 얼굴 정보
  storedPersons: Array         // HomeView에서 전달된 저장된 인물 목록
});

const emits = defineEmits(['updateStoredPersons']);  // 저장된 인물 목록을 HomeView에 전달

// 사용자 입력 값
const inputId = ref('');
const inputName = ref('');

// InfoPanel 스타일 정의 (가로 30%)
const infoPanelStyle = computed(() => ({
  width: '30%',
  padding: '1rem',
  backgroundColor: '#f5f5f5',
  display: 'flex',
  flexDirection: 'column',
}));

// 감지된 얼굴 정보를 저장하는 함수
const saveDetectedPerson = () => {
  if (!props.detectedDescriptor || !inputId.value || !inputName.value) return;

  const newPerson = {
    id: inputId.value,
    name: inputName.value,
    descriptor: props.detectedDescriptor.descriptor,  // CameraView에서 전달된 descriptor 사용
  };

  emits('updateStoredPersons', [...props.storedPersons, newPerson]);  // HomeView로 업데이트된 데이터 전달

  // 입력 초기화
  inputId.value = '';
  inputName.value = '';
};
</script>

<style scoped>
/* 추가적인 스타일 정의 */
</style>
