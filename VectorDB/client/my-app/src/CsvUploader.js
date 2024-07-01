import React, { useState } from 'react';
import axios from 'axios';

function CsvUploader() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/upload-csv/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('File uploaded successfully: ' + response.data.message);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const handleQuerySubmit = async () => {
    try {
      const response = await axios.get('http://localhost:8001/query/', {
        params: { query_text: query },
      });
      setResults(response.data.results);
    } catch (error) {
      console.error('Error querying database:', error);
    }
  };

  return (
    <div className="CsvUploader">
      <h1>FastAPI와 React 연동</h1>

      <div>
        <h2>CSV 파일 업로드</h2>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleFileUpload}>업로드</button>
      </div>

      <div>
        <h2>쿼리 입력</h2>
        <input type="text" value={query} onChange={handleQueryChange} />
        <button onClick={handleQuerySubmit}>쿼리 전송</button>
      </div>

      <div>
        <h2>결과</h2>
        <ul>
          {results.map((result, index) => (
            <li key={index}>
              <p>ID: {result.id}</p>
              <p>Document: {result.document}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default CsvUploader;