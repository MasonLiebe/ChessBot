import React, { useState } from 'react';
import './App.css';
import { PieceWorkshop } from './components/PieceWorkshop/PieceWorkshop';
import { GameWorkshop } from './components/GameWorkshop/GameWorkshop';
import { PlayBot } from './components/PlayBot/PlayBot';
import { standardBoard } from './constants';
import { MovementPattern, DefaultCustomPatterns } from './components/MovementPattern';

function App() {
  const [activeWorkshop, setActiveWorkshop] = useState('piece');
  const [game_rows, setGameRows] = useState(8);
  const [game_cols, setGameCols] = useState(8);
  const [game_pieces, setGamePieces] = useState<string[]>(standardBoard.split(''));
  const [moveMentPatterns, setMovementPatterns] = useState<MovementPattern[]>(DefaultCustomPatterns);

  const handleWorkshopChange = (workshop: React.SetStateAction<string>) => {
    setActiveWorkshop(workshop);
  };

  const startGame = () => {
    setGameRows(8);
    setGameCols(8);
    setGamePieces(standardBoard.split(''));
    setActiveWorkshop('play');
  };

  const handleSendPiece = () => {
    console.log('sendpiece')
  }
  return (
    <div className="app">
      <nav className="navbar">
        <ul className="navbar-nav">
          <li
            className={`nav-item ${activeWorkshop === 'piece' ? 'active' : ''}`}
            onClick={() => handleWorkshopChange('piece')}
          >
            Customize Pieces
          </li>
          <li
            className={`nav-item ${activeWorkshop === 'game' ? 'active' : ''}`}
            onClick={() => handleWorkshopChange('game')}
          >
            Customize Game
          </li>
          <li
            className={`nav-item ${activeWorkshop === 'play' ? 'active' : ''}`}
            onClick={() => handleWorkshopChange('play')}
          >
            Play Vs. Bot
          </li>
        </ul>
      </nav>
      <div className="content-container">
        <div className="workshop-container">
          <div style={{ display: activeWorkshop === 'piece' ? 'block' : 'none' }}>
            <PieceWorkshop
              movementPatterns={movementPatterns}
              updateMovementPatterns={updateMovementPatterns}
            />
          </div>
          <div style={{ display: activeWorkshop === 'game' ? 'block' : 'none' }}>
            <GameWorkshop
              gameRows={gameRows}
              gameColumns={gameColumns}
              gamePieces={gamePieces}
              updateGameRows={updateGameRows}
              updateGameColumns={updateGameColumns}
              updateGamePieces={updateGamePieces}
              startGame={startGame}
            />
          </div>
          <div style={{ display: activeWorkshop === 'play' ? 'block' : 'none' }}>
            <PlayBot
              gameRows={gameRows}
              gameColumns={gameColumns}
              gamePieces={gamePieces}
              movementPatterns={movementPatterns}
            />
          </div>
        </div>
      </div>
      <div className="footer">
        <p>
          Made for fun by Mason Liebe&nbsp;
          <a
            href="https://github.com/MasonLiebe/ChessBot"
            target="_blank"
            className="github-link"
          >
            <img
              src={`assets/github.png`}
              alt="githublogo"
              className="github-logo"
            />
          </a>
        </p>
      </div>
    </div>
  );
}

export default App;