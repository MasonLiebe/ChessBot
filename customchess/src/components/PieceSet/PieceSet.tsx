import React from 'react';
import './PieceSet.css';

interface PieceSetProps {
  color: 'black' | 'white';
}

function PieceSet({ color }: PieceSetProps) {
  const pieces = [
    'pawn',
    'knight',
    'bishop',
    'rook',
    'queen',
    'custom1',
    'custom2',
    'custom3',
    'custom4',
    'custom5',
    'custom6',
  ];

  return (
    <div className="piece-set">
      {pieces.map((piece) => (
        <img
          key={piece}
          src={`/assets/pieces/${color}-${piece}.png`}
          alt={`${color} ${piece}`}
          className="piece"
        />
      ))}
    </div>
  );
}

export default PieceSet;