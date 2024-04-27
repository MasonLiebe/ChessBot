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
        <div className="navbar-brand">Custom Chess</div>
        <ul className="navbar-nav">
          <li
            className={`nav-item ${activeWorkshop === 'piece' ? 'active' : ''}`}
            onClick={() => handleWorkshopChange('piece')}
          >
            Piece Workshop
          </li>
          <li
            className={`nav-item ${activeWorkshop === 'game' ? 'active' : ''}`}
            onClick={() => handleWorkshopChange('game')}
          >
            Game Workshop
          </li>
        </ul>
      </nav>
      <div className="workshop-container">
        {activeWorkshop === 'piece' ? <PieceWorkshop /> : <GameWorkshop />}
      </div>
    </div>
  );
}

export default App;