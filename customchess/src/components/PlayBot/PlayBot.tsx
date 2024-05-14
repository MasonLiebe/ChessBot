import React, { useState, useEffect } from 'react';
import './PlayBot.css';
import CustomGameBoard from '../CustomGameBoard/CustomGameBoard';
import PlayPanel from '../PlayPanel/PlayPanel';
import { standardBoard } from '../../constants';

export function PlayBot() {
  const [rows, setRows] = useState(8);
  const [columns, setColumns] = useState(8);
  const [pieces, setPieces] = useState<string[]>(standardBoard.split(''));
  const [selectedBoardPiece, setSelectedBoardPiece] = useState<number | null>(null);
  const [botThinkTime, setBotThinkTime] = useState(5);

  const initalizeBoard = (
    rows: number,
    columns: number,
    pieces: string[]
    ) => {
      setRows(rows);
      setColumns(columns);
      setPieces(pieces);
    };

  const handleBotThinkTimeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newBotThinkTime = parseInt(event.target.value);
    setBotThinkTime(newBotThinkTime);
  };

  const handleBoardClick = (index: number) => {
    console.log(index);
    if (selectedBoardPiece !== null) {
      // Move the selected board piece to the clicked square
      const updatedPieces = [...pieces];
      updatedPieces[index] = pieces[selectedBoardPiece];
      updatedPieces[selectedBoardPiece] = '.';
      setPieces(updatedPieces);
      setSelectedBoardPiece(null);
    } else {
      // Select the clicked board piece
      if (pieces[index] !== '.') {
        setSelectedBoardPiece(index);
      }
    }
  };

  const handleUndoMove = () => {
    // Undo the last move
  }

  const handleGetEngineMove = () => {
    // Get the engine move
  }

  const handleFlipBoard = () => {
    // Flip the board
  }

  const handleResetGame = () => {
    // Reset the game
  }

  return (
    <div className="app">
      <div className="main-container-game">
        <div className="chessboard-wrapper-game">
          <div className="chessboard-container-game">
            <CustomGameBoard
              rows={rows}
              columns={columns}
              pieces={pieces}
              selected={selectedBoardPiece}
              onSquareClick={handleBoardClick}
            />
          </div>
        </div>
        <div>
          <PlayPanel
            botThinkTime = {botThinkTime}
            onBotThinkTimeChange = {handleBotThinkTimeChange}
            onUndoMove = {handleUndoMove}
            onGetEngineMove = {handleGetEngineMove}
            onFlipBoard = {handleFlipBoard}
            onResetGame = {handleResetGame}
          />
        </div>
      </div>
    </div>
  );
}
