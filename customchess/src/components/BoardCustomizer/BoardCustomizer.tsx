import React, { useState, useRef, useEffect } from 'react';
import './BoardCustomizer.css';

interface BoardCustomizerProps {
  rows: number;
  columns: number;
  pieces: string[]; // 256 character string representing the board
  selected: number | null;
  onSquareClick: (index: number) => void;
}

interface PieceToImageMap {
  [key: string]: string;
}

const piece_to_image: PieceToImageMap = {
  'p': 'black-pawn',
  'n': 'black-knight',
  'b': 'black-bishop',
  'r': 'black-rook',
  'q': 'black-queen',
  'k': 'black-king',
  'a': 'black-custom1',
  'c': 'black-custom2',
  'd': 'black-custom3',
  'e': 'black-custom4',
  'f': 'black-custom5',
  'g': 'black-custom6',
  'P': 'white-pawn',
  'N': 'white-knight',
  'B': 'white-bishop',
  'R': 'white-rook',
  'Q': 'white-queen',
  'K': 'white-king',
  'A': 'white-custom1',
  'C': 'white-custom2',
  'D': 'white-custom3',
  'E': 'white-custom4',
  'F': 'white-custom5',
  'G': 'white-custom6'
};


export default function BoardCustomizer({ rows, columns, pieces, selected, onSquareClick}: BoardCustomizerProps) {
  const squareSize = Math.floor(690 / Math.max(rows, columns));
  const boardWidth = columns * squareSize;
  const boardHeight = rows * squareSize;
  const [isDragging, setIsDragging] = useState(false);
  const [startIndex, setStartIndex] = useState<number | null>(null);
  const [isMouseUp, setIsMouseUp] = useState(false);
  const boardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleMouseLeave = () => {
      setIsDragging(false);
    };

    const boardElement = boardRef.current;
    if (boardElement) {
      boardElement.addEventListener('mouseleave', handleMouseLeave);
    }

    return () => {
      if (boardElement) {
        boardElement.removeEventListener('mouseleave', handleMouseLeave);
      }
    };
  }, []);

  const handleMouseEnter = (index: number) => {
    if (isDragging && startIndex !== null && startIndex !== index) {
      onSquareClick(index);
    }
  };

  const handleMouseDown = (index: number) => {
    setIsDragging(true);
    setStartIndex(index);
    setIsMouseUp(false);
    onSquareClick(index);
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    setIsMouseUp(true);
  };

  const handleClick = (index: number) => {
    if (startIndex === index && isMouseUp) {
      onSquareClick(index);
    }
  };

  const renderSquares = () => {
    const squares = [];
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < columns; col++) {
        const squareColor = (row + col) % 2 === 0 ? 'white' : 'black';
        const index = (rows - row - 1) * 16 + columns - col - 1;
        const piece = pieces[index];

        squares.push(
          <div
            key={`${row}-${col}`}
            className={`square ${squareColor} ${index === selected ? 'selected' : ''}`}
            style={{
              width: `${squareSize}px`,
              height: `${squareSize}px`,
            }}
            onMouseEnter={() => handleMouseEnter(index)}
            onMouseDown={() => handleMouseDown(index)}
            onMouseUp={handleMouseUp}
          >
            {piece !== '.' && piece_to_image[piece] && (
              <img
                src={`/assets/pieces/${piece_to_image[piece]}.png`}
                alt={`${piece}`}
                className="piece"
              />
            )}
          </div>
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