import React, { useState, useEffect } from 'react';
import './PlayBot.css';
import CustomGameBoard from '../CustomGameBoard/CustomGameBoard';
import PlayPanel from '../PlayPanel/PlayPanel';
import { standardBoard } from '../../constants';

interface playBotProps {
  init_rows: number;
  init_columns: number;
  init_pieces: string[];
}

export function PlayBot({ init_rows, init_columns, init_pieces }: playBotProps) {
  const [rows, setRows] = useState(init_rows);
  const [columns, setColumns] = useState(init_columns);
  const [pieces, setPieces] = useState<string[]>(init_pieces);
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
