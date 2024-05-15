import React, { useState, useEffect } from 'react';
import './GameWorkshop.css';
import BoardCustomizer from '../BoardCustomizer/BoardCustomizer';
import BoardPanel from '../BoardPanel/BoardPanel';
import PieceSet from '../PieceSet/PieceSet';
import { standardBoard } from '../../constants';
import { start } from 'repl';

interface GameWorkshopProps {
  gameRows: number;
  gameColumns: number;
  gamePieces: String[];
  updateGameRows: (rows : number) => void;
  updateGameColumns: (cols : number) => void;
  updateGamePieces: (pieces : string[]) => void;
  startGame: () => void;
}

export function GameWorkshop({ gameRows, gameColumns, gamePieces, updateGameRows, updateGameColumns, updateGamePieces, startGame }: GameWorkshopProps) {
  const [rows, setRows] = useState(gameRows);
  const [columns, setColumns] = useState(gameColumns);
  const [isSquare, setIsSquare] = useState(true);
  const [pieces, setPieces] = useState<string[]>(standardBoard.split(''));
  const [selectedPieceType, setSelectedPieceType] = useState<{ piece: string; color: string } | null>(null);
  const [selectedBoardPiece, setSelectedBoardPiece] = useState<number | null>(null);

  const handlePieceSelect = (piece: string | null, color: string) => {
    if (piece) {
      setSelectedBoardPiece(null);
      setSelectedPieceType({ piece, color });
    } else {
      setSelectedPieceType(null);
    }
  };

  const handleRowsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newRows = parseInt(event.target.value);
    if (isSquare) {
      setColumns(newRows)
      updateGameColumns(newRows);
    }
    setRows(newRows)
    updateGameRows(newRows)
  };

  const handleColumnsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newColumns = parseInt(event.target.value);
    setColumns(newColumns)
    updateGameColumns(newColumns);
    if (isSquare) {
      setRows(newColumns)
      updateGameRows(newColumns);
    }
  };

  const handleSquareToggle = () => {
    setIsSquare(!isSquare);
    if (!isSquare) {
      updateGameColumns(8);
      updateGameRows(8);
      setRows(8)
      setColumns(8)
    }
  };

  const handleBoardClick = (index: number) => {
    console.log(index);
    if (selectedBoardPiece !== null) {
      // Move the selected board piece to the clicked square
      const updatedPieces = [...pieces];
      updatedPieces[index] = pieces[selectedBoardPiece];
      updatedPieces[selectedBoardPiece] = '.';
      setPieces(updatedPieces);
      updateGamePieces(updatedPieces)
      setSelectedBoardPiece(null);
    } else if (selectedPieceType) {
      // Check if the clicked square already has the selected piece
      if (pieces[index] === selectedPieceType.piece) {
        // Remove the piece from the board
        const updatedPieces = [...pieces];
        updatedPieces[index] = '.';
        setPieces(updatedPieces);
        updateGamePieces(updatedPieces);
      } else {
        // Place the selected piece type on the clicked square
        const updatedPieces = [...pieces];
        console.log(selectedPieceType.piece);
        updatedPieces[index] = selectedPieceType.piece;
        setPieces(updatedPieces);
        updateGamePieces(updatedPieces);
      }
    } else {
      // Select the clicked board piece
      if (pieces[index] !== '.') {
        setSelectedBoardPiece(index);
      }
    }
  }

  const handleStartGame = () => {
    // Check if each player has exactly one king on the board
    let blackKingFound = false;
    let whiteKingFound = false;

    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < columns; col++) {
        const index = (rows - row - 1) * 16 + columns - col - 1;
        if (pieces[index] === 'k') {
          if (blackKingFound) {
            console.log('Black has more than one king');
            return;
          }
          blackKingFound = true;
        }
        if (pieces[index] === 'K') {
          if (whiteKingFound) {
            console.log('White has more than one king');
            return;
          }
          whiteKingFound = true;
        }
      }
    }
    
    if (!blackKingFound) {
      console.log('Black has no king');
      return;
    }
    if (!whiteKingFound) {
      console.log('White has no king');
      return;
    }
    
    startGame();

  }

  const handleUploadGameMode = () => {
    console.log('Upload Game Mode');
  }

  return (
    <div className="app">
      <div className="main-container">
        <div className="chessboard-wrapper">
          <div className="chessboard-container">
            <PieceSet color="black" selectedPiece={selectedPieceType} onPieceSelect={handlePieceSelect} />
            <BoardCustomizer
              rows={rows}
              columns={columns}
              pieces={pieces}
              selected={selectedBoardPiece}
              onSquareClick={handleBoardClick}
            />
            <PieceSet color="white" selectedPiece={selectedPieceType} onPieceSelect={handlePieceSelect}/>
          </div>
        </div>
        <BoardPanel
          rows={rows}
          columns={columns}
          isSquare={isSquare}
          onRowsChange={handleRowsChange}
          onColumnsChange={handleColumnsChange}
          onSquareToggle={handleSquareToggle}
          onClearBoard={() => setPieces(Array(rows * columns).fill('.'))}
          onResetBoard={() => setPieces(standardBoard.split(''))}
          onStartGame={handleStartGame}
          onUploadGameMode={handleUploadGameMode}
          selected={selectedPieceType}
        />
      </div>
    </div>
  );
}
