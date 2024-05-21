import React, { useState, useEffect } from 'react';
import './PlayBot.css';
import CustomGameBoard from '../CustomGameBoard/CustomGameBoard';
import PlayPanel from '../PlayPanel/PlayPanel';
import { standardBoard } from '../../constants';
import { MovementPattern } from '../MovementPattern';

interface playBotProps {
  gameRows: number;
  gameColumns: number;
  gamePieces: string[];
  gameMovementPatterns: MovementPattern[]
}

export function PlayBot({ gameRows, gameColumns, gamePieces, gameMovementPatterns }: playBotProps) {
  const [rows, setRows] = useState(gameRows);
  const [columns, setColumns] = useState(gameColumns);
  const [pieces, setPieces] = useState<string[]>(gamePieces);
  const [movementPatterns, setMovementPatterns] = useState<MovementPattern[]>(gameMovementPatterns)
  const [selectedBoardPiece, setSelectedBoardPiece] = useState<number | null>(null);
  const [botThinkTime, setBotThinkTime] = useState(5);
  const [isWhiteTurn, setIsWhiteTurn] = useState(true);
  const [isGameOver, setIsGameOver] = useState(false);

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

  const getLegalMoves = (piece: string, index: number) => {
    // Get the legal moves for the selected piece from the engine
  }

  const makeUserMove = (index: number) => {
    // Make the user move
  }

  const makeEngineMove = () => {
    // Make the engine move
  }

  useEffect(() => {
    setRows(gameRows);
    setColumns(gameColumns);
    setPieces(gamePieces);
    setMovementPatterns(gameMovementPatterns);
  }, [gameRows, gameColumns, gamePieces, gameMovementPatterns]);

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
