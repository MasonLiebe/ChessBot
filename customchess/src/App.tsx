import React, { useState } from 'react';
import './App.css';
import { PieceWorkshop } from './components/PieceWorkshop/PieceWorkshop';
import { GameWorkshop } from './components/GameWorkshop/GameWorkshop';

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
        </ul>
      </nav>
      <div className="workshop-container">
        <div style={{ display: activeWorkshop === 'piece' ? 'block' : 'none' }}>
          <PieceWorkshop />
        </div>
        <div style={{ display: activeWorkshop === 'game' ? 'block' : 'none' }}>
          <GameWorkshop />
        </div>
      </div>
    </div>
  );
}

export default App;