import React, { useState } from 'react';
import './App.css';
import PieceCustomizer from './components/PieceCustomizer/PieceCustomizer';
import PiecePanel from './components/PiecePanel/PiecePanel';
import CustomPieceSet from './components/CustomPIeceSet/CustomPieceSet';
import { GameWorkshop } from './components/GameWorkshop/GameWorkshop';
import { PieceWorkshop } from './components/PieceWorkshop/PieceWorkshop';

function App() {
  return PieceWorkshop();
}

export default App;

