import React, { useState } from 'react';

import './App.css';

import Chessboard from './components/Chessboard/Chessboard';

function App() {
  const [rows, setRows] = useState(8);
  const [columns, setColumns] = useState(8);

  const handleRowsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRows(parseInt(event.target.value));
  };

  const handleColumnsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setColumns(parseInt(event.target.value));
  };

  return (
    <div className="app">
      <div className="chessboard-container">
        <Chessboard rows={rows} columns={columns} />
      </div>
      <div className="slider-container">
        <div className="slider">
          <label htmlFor="rows-slider">Rows: {rows}</label>
          <input
            id="rows-slider"
            type="range"
            min="1"
            max="16"
            value={rows}
            onChange={handleRowsChange}
          />
        </div>
        <div className="slider">
          <label htmlFor="columns-slider">Columns: {columns}</label>
          <input
            id="columns-slider"
            type="range"
            min="1"
            max="16"
            value={columns}
            onChange={handleColumnsChange}
          />
        </div>
      </div>
    </div>
  );
}
export default App;