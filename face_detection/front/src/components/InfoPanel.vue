<template>
  <div :style="infoPanelStyle">
    <h3>인물 정보 저장</h3>

    <p v-if="detectedDescriptor">
      얼굴 벡터 감지됨. 정보를 입력하고 저장하세요.
    </p>
    <p v-else>감지된 얼굴이 없습니다.</p>
    <input v-model="inputId" placeholder="ID 입력" />
    <input v-model="inputName" placeholder="이름 입력" />
    <button @click="saveDetectedPerson">저장</button>



    <!-- 감지된 인물 정보를 우측에 표시 -->
    <div v-if="detectedPerson">
      <h3>감지된 인물 정보</h3>
      <p>ID: {{ detectedPerson.id }}</p>
      <p>이름: {{ detectedPerson.name }}</p>
    </div>
    
    <h3>저장된 인물 목록</h3>
    <ul>
      <li v-for="person in storedPersons" :key="person.id">
        {{ person.id }} - {{ person.name }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  detectedDescriptor: Object,  // 감지된 얼굴 디스크립터
  storedPersons: Array         // 저장된 인물 목록
});
const emits = defineEmits(['updateStoredPersons']);

// 감지된 인물 정보
const detectedPerson = ref<{ id: string, name: string } | null>(null);

const inputId = ref('');
const inputName = ref('');

const infoPanelStyle = computed(() => ({
  width: '30%',
  padding: '1rem',
  backgroundColor: '#f5f5f5',
  display: 'flex',
  flexDirection: 'column',
}));

// 감지된 인물 정보를 저장하는 함수
const saveDetectedPerson = () => {
  if (!props.detectedDescriptor || !inputId.value || !inputName.value) return;

  const newPerson = {
    id: inputId.value,
    name: inputName.value,
    descriptor: props.detectedDescriptor  // 감지된 디스크립터 저장
  };

  // 감지된 인물 정보 업데이트
  detectedPerson.value = { id: inputId.value, name: inputName.value };

  // 새로운 인물을 기존의 저장된 목록에 추가하고, HomeView에 업데이트
  emits('updateStoredPersons', [...props.storedPersons, newPerson]);

  // 입력 초기화
  inputId.value = '';
  inputName.value = '';
};
</script>

<style scoped>
/* 추가적인 스타일 정의 */
</style>