import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// 메인 컴포넌트
function App() {
  // 파일1, 파일2, 결과 상태 관리
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState(null);

  // 파일1 변경 핸들러
  const handleFileChange1 = (e) => {
    setFile1(e.target.files[0]);
  };

  // 파일2 변경 핸들러
  const handleFileChange2 = (e) => {
    setFile2(e.target.files[0]);
  };

  // 폼 제출 핸들러
  const handleSubmit = async (e) => {
    e.preventDefault(); // 기본 폼 제출 동작 막기
    const formData = new FormData();
    formData.append('file1', file1); // 파일1 추가
    formData.append('file2', file2); // 파일2 추가

    try {
      // 서버에 POST 요청 보내기
      const response = await axios.post('http://localhost:8001/compare-images', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data); // 결과 상태에 응답 데이터 저장
    } catch (error) {
      console.error(error); // 에러 발생 시 콘솔에 출력
    }
  };

  return (
    <div className="App">
      <h1>Image Comparison API</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="file1">Upload Image 1:</label>
        <input type="file" id="file1" name="file1" accept="image/*" onChange={handleFileChange1} required /><br /><br />
        <label htmlFor="file2">Upload Image 2:</label>
        <input type="file" id="file2" name="file2" accept="image/*" onChange={handleFileChange2} required /><br /><br />
        <button type="submit">Compare Images</button>
      </form>
      <h2>Result:</h2>
      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre> // 결과 JSON 형식으로 출력
      )}
    </div>
  );
}

export default App;