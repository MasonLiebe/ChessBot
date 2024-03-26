import React from 'react';

import './Chessboard.css';

interface ChessboardProps {
  rows: number;
  columns: number;
}

export default function Chessboard({ rows, columns }: ChessboardProps) {
  const squareSize = Math.floor(800 / Math.max(rows, columns));
  const boardWidth = columns * squareSize;
  const boardHeight = rows * squareSize;

  const renderSquares = () => {
    const squares = [];

    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < columns; col++) {
        const squareColor = (row + col) % 2 === 0 ? 'white' : 'black';
        squares.push(
          <div
            key={`${row}-${col}`}
            className={`square ${squareColor}`}
            style={{
              width: `${squareSize}px`,
              height: `${squareSize}px`,
            }}
          ></div>
        );
      }
    }

    return squares;
  };

  return (
    <div className="chessboard-wrapper">
      <div
        id="chessboard"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${columns}, 1fr)`,
          gridTemplateRows: `repeat(${rows}, 1fr)`,
          width: `${boardWidth}px`,
          height: `${boardHeight}px`,
        }}
      >
        {renderSquares()}
      </div>
    </div>
  );
}