import React from 'react';
import './App.css';
import ImageComparison from './ImageComparison';
import CsvUploader from './CsvUploader';

function App() {
  return (
    <div className="App">
      <ImageComparison />
      <CsvUploader />
    </div>
  );
}

export default App;