import React from 'react';
import './PieceCustomizer.css';

interface PieceCustomizerProps {
  size: number; // odd number up to 31
  piece: string; // 256 character string representing the board
  attack_north: boolean;
  attack_east: boolean;
  attack_south: boolean;
  attack_west: boolean;
  attack_southEast: boolean;
  attack_southWest: boolean;
  attack_northEast: boolean;
  attack_northWest: boolean;
  translate_north: boolean;
  translate_east: boolean;
  translate_south: boolean;
  translate_west: boolean;
  translate_southEast: boolean;
  translate_southWest: boolean;
  translate_northEast: boolean;
  translate_northWest: boolean;
  attack_jumps: number[];
  translate_jumps: number[];
  attack_slides: number[][];
  translate_slides: number[][];
  onSquareClick: (row: number, col: number) => void;
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
  

function PieceCustomizer({
  size,
  piece,
  attack_north,
  attack_east,
  attack_south,
  attack_west,
  attack_southEast,
  attack_southWest,
  attack_northEast,
  attack_northWest,
  translate_north,
  translate_east,
  translate_south,
  translate_west,
  translate_southEast,
  translate_southWest,
  translate_northEast,
  translate_northWest,
  attack_jumps,
  translate_jumps,
  attack_slides,
  translate_slides,
  onSquareClick,
}: PieceCustomizerProps) {
  const squareSize = Math.floor(600 / size);
  const boardWidth = size * squareSize;
  const boardHeight = size * squareSize;

  const highlightColor = (y: number, x: number) => {
    if (x === 0 && y > 0) { // north
      if (attack_north && translate_north) {
        return 'purple';
      } else if (attack_north) {
        return 'red';
      } else if (translate_north) {
        return 'blue';
      } else {
        return null;
      }
    } else if (x === 0 && y < 0) { // south
      if (attack_south && translate_south) {
        return 'purple';
      } else if (attack_south) {
        return 'red';
      } else if (translate_south) {
        return 'blue';
      } else {
        return null;
      }
    } else if (y === 0 && x > 0) { // east
      if (attack_east && translate_east) {
        return 'purple';
      } else if (attack_east) {
        return 'red';
      } else if (translate_east) {
        return 'blue';
      } else {
        return null;
      }
    } else if (y === 0 && x < 0) { // west
      if (attack_west && translate_west) {
        return 'purple';
      } else if (attack_west) {
        return 'red';
      } else if (translate_west) {
        return 'blue';
      } else {
        return null;
      }
    }
    if (x === y && x > 0) { // north east
      if (attack_northEast && translate_northEast) {
        return 'purple';
      } else if (attack_northEast) {
        return 'red';
      } else if (translate_northEast) {
        return 'blue';
      } else {
        return null;
      }
    } else if (x === y && x < 0) { // south west
      if (attack_southWest && translate_southWest) {
        return 'purple';
      } else if (attack_southWest) {
        return 'red';
      } else if (translate_southWest) {
        return 'blue';
      } else {
        return null;
      }
    } else if (x === -y && x > 0) { // south east
      if (attack_southEast && translate_southEast) {
        return 'purple';
      } else if (attack_southEast) {
        return 'red';
      } else if (translate_southEast) {
        return 'blue';
      } else {
        return null;
      }
    } else if (x === -y && x < 0) { // north west
      if (attack_northWest && translate_northWest) {
        return 'purple';
      } else if (attack_northWest) {
        return 'red';
      } else if (translate_northWest) {
        return 'blue';
      } else {
        return null;
      }
    } else {
      return null;
    }
  };

  const renderSquares = () => {
    const squares = [];
    const centerIndex = Math.floor(size / 2);
  
    for (let row = 0; row < size; row++) {
      for (let col = 0; col < size; col++) {
        const squareColor = (row + col) % 2 === 0 ? 'white' : 'black';
        const isCenterSquare = row === centerIndex && col === centerIndex;
        const squareRow = centerIndex - row;
        const squareCol = col - centerIndex;
        const highlightColorValue = highlightColor(squareRow, squareCol);
  
        squares.push(
          <div
            key={`${squareRow}-${squareCol}`}
            className={`square ${squareColor} ${isCenterSquare ? 'center' : ''} ${
              highlightColorValue ? 'highlighted' : ''
            }`}
            style={{
              width: `${squareSize}px`,
              height: `${squareSize}px`,
            }}
            data-highlight-color={highlightColorValue || ''}
            onClick={() => onSquareClick(squareRow, squareCol)}
          >
            {isCenterSquare && piece_to_image[piece] && (
              <img
                src={`/assets/pieces/${piece_to_image[piece]}.png`}
                alt={piece}
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
    <div className="piece-customizer">
      <div
        className="board"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${size}, 1fr)`,
          gridTemplateRows: `repeat(${size}, 1fr)`,
          width: `${boardWidth}px`,
          height: `${boardHeight}px`,
        }}
      >
        {renderSquares()}
      </div>
    </div>
  );
}

export default PieceCustomizer;