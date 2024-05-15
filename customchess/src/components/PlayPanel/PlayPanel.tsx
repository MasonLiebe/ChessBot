import React from 'react';
import './PlayPanel.css';

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

interface PlayPanelProps {
  botThinkTime: number;
  onBotThinkTimeChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onUndoMove: () => void;
  onGetEngineMove: () => void;
  onFlipBoard: () => void;  
  onResetGame: () => void;
}

function PlayPanel({
  botThinkTime,
  onBotThinkTimeChange,
  onUndoMove,
  onGetEngineMove,
  onFlipBoard,
  onResetGame
}: PlayPanelProps) {
  return (
    <div className="play-panel">
      <div className="board-panel-title">Game Properties</div>
      <div className="slider">
        <label htmlFor="rows-slider">Think Time (s) {botThinkTime}</label>
        <input
          id="rows-slider"
          type="range"
          min="1"
          max="100git "
          value={botThinkTime}
          onChange={onBotThinkTimeChange}
        />
      </div>
      <button className="game-button" onClick={onUndoMove}>Undo Move</button>
      <button className="game-button" onClick={onGetEngineMove}>Get Engine Move</button>
      <button className="game-button" onClick={onFlipBoard}>Flip Board</button>
      <button className="game-button" onClick={onResetGame}>Reset Game</button>
    </div>
  );
}

export default PlayPanel;