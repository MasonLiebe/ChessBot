import React, { useState } from 'react';
import './PieceSet.css';

interface PieceSetProps {
  color: 'black' | 'white';
  onPieceSelect: (piece: string) => void;
}

function PieceSet({ color, onPieceSelect }: PieceSetProps) {
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

  const [selectedPiece, setSelectedPiece] = useState<string | null>(null);

  const handlePieceClick = (piece: string) => {
    setSelectedPiece(piece);
    onPieceSelect(piece, color);
  };

  return (
    <div className="piece-set">
      {pieces.map((piece) => (
        <img
          key={piece}
          src={`/assets/pieces/${color}-${piece}.png`}
          alt={`${color} ${piece}`}
          className={`piece ${selectedPiece === piece ? 'selected' : ''}`}
          onClick={() => handlePieceClick(piece)}
        />
      ))}
    </div>
  );
}

export default PieceSet;