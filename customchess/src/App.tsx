import React, { useState } from 'react';
import './App.css';
import { PieceWorkshop } from './components/PieceWorkshop/PieceWorkshop';
import { GameWorkshop } from './components/GameWorkshop/GameWorkshop';
import { PlayBot } from './components/PlayBot/PlayBot';
import { standardBoard } from './constants';

function App() {
  const [activeWorkshop, setActiveWorkshop] = useState('piece');
  const [game_rows, setGameRows] = useState(8);
  const [game_cols, setGameCols] = useState(8);
  const [game_pieces, setGamePieces] = useState<string[]>(standardBoard.split(''));
  const [movement_patterns, setMovementPatterns] = useState<string[]>(['']);

  const handleWorkshopChange = (workshop: React.SetStateAction<string>) => {
    setActiveWorkshop(workshop);
  };

  const startGame = () => {
    setGameRows(8);
    setGameCols(8);
    setGamePieces(standardBoard.split(''));
    setActiveWorkshop('play');
  };

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
      <div className="workshop-container">
        <div style={{ display: activeWorkshop === 'piece' ? 'block' : 'none' }}>
          <PieceWorkshop />
        </div>
        <div style={{ display: activeWorkshop === 'game' ? 'block' : 'none' }}>
          <GameWorkshop
            startGame={startGame}
          />
        </div>
        <div style={{ display: activeWorkshop === 'play' ? 'block' : 'none' }}>
          <PlayBot
           init_rows = {game_rows}
           init_columns = {game_cols}
           init_pieces={game_pieces}/>
        </div>
      </div>
      <div className="footer">
        <p>
          Made for fun by Mason Liebe
          <a
            href="https://github.com/MasonLiebe?tab=overview&from=2024-04-01&to=2024-04-29"
            target="_blank"
            color='white'
          >Mason Liebe</a>
        </p>
      </div>
    </div>
  );
}

export default App;