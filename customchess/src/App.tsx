import React, { useState } from 'react';
import './App.css';
import { PieceWorkshop } from './components/PieceWorkshop/PieceWorkshop';
import { GameWorkshop } from './components/GameWorkshop/GameWorkshop';
import { PlayBot } from './components/PlayBot/PlayBot';

function App() {
  const [activeWorkshop, setActiveWorkshop] = useState('piece');

  const handleWorkshopChange = (workshop: React.SetStateAction<string>) => {
    setActiveWorkshop(workshop);
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
          <GameWorkshop />
        </div>
        <div style={{ display: activeWorkshop === 'play' ? 'block' : 'none' }}>
          <PlayBot />
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