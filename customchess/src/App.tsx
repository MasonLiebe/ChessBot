import React, { useState, useEffect } from 'react';
import './App.css';
import Chessboard from './components/Chessboard/Chessboard';
import BoardPanel from './components/BoardPanel/BoardPanel';
import PieceSet from './components/PieceSet/PieceSet';
import { standardBoard } from './constants';

function App() {
  const [rows, setRows] = useState(8);
  const [columns, setColumns] = useState(8);
  const [isSquare, setIsSquare] = useState(true);

  const handleRowsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newRows = parseInt(event.target.value);
    setRows(newRows);
    if (isSquare) {
      setColumns(newRows);
    }
  };

  const handleColumnsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newColumns = parseInt(event.target.value);
    setColumns(newColumns);
    if (isSquare) {
      setRows(newColumns);
    }
  };

  const handleSquareToggle = () => {
    setIsSquare(!isSquare);
    if (!isSquare) {
      setRows(8);
      setColumns(8);
    }
  };

  useEffect(() => {
    if (isSquare) {
      setColumns(rows);
    }
  }, [isSquare, rows]);

  return (
    <div className="app">
      <h1 className="app-title">Custom Chess Workshop</h1>
      <div className="main-container">
        <div className="chessboard-wrapper">
          <div className="chessboard-container">
            <PieceSet color="black" />
            <Chessboard rows={rows} columns={columns} pieces = {standardBoard} initialPieces= {standardBoard}/>
            <PieceSet color="white" />
          </div>

        </div>
        <BoardPanel
          rows={rows}
          columns={columns}
          isSquare={isSquare}
          onRowsChange={handleRowsChange}
          onColumnsChange={handleColumnsChange}
          onSquareToggle={handleSquareToggle}
        />
      </div>
    </div>
  );
}

export default App;