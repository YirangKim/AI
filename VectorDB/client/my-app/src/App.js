import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange1 = (e) => {
    setFile1(e.target.files[0]);
  };

  const handleFileChange2 = (e) => {
    setFile2(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);

    try {
      const response = await axios.post('http://localhost:8000/compare-images', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
      setError(null);
    } catch (error) {
      console.error(error);
      setError('An error occurred while comparing images.');
      setResult(null);
    }
  };

  return (
    <div className="App">
      <h1>이미지 유사도판단 테스트</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="file1">Upload Image 1:</label>
        <input type="file" id="file1" name="file1" accept="image/*" onChange={handleFileChange1} required /><br /><br />
        <label htmlFor="file2">Upload Image 2:</label>
        <input type="file" id="file2" name="file2" accept="image/*" onChange={handleFileChange2} required /><br /><br />
        <button type="submit">Compare Images</button>
      </form>
      <h2>Result:</h2>
      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
      {error && (
        <p style={{ color: 'red' }}>{error}</p>
      )}
    </div>
  );
}

export default App;