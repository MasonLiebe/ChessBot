import React, { useState } from 'react';
import './App.css';
import PieceCustomizer from './components/PieceCustomizer/PieceCustomizer';
import PiecePanel from './components/PiecePanel/PiecePanel';
import CustomPieceSet from './components/CustomPIeceSet/CustomPieceSet';

function App() {
  const [size, setSize] = useState(15);
  const [attack_north, setAttackNorth] = useState(false);
  const [attack_east, setAttackEast] = useState(false);
  const [attack_south, setAttackSouth] = useState(false);
  const [attack_west, setAttackWest] = useState(false);
  const [attack_southEast, setAttackSouthEast] = useState(false);
  const [attack_southWest, setAttackSouthWest] = useState(false);
  const [attack_northEast, setAttackNorthEast] = useState(false);
  const [attack_northWest, setAttackNorthWest] = useState(false);
  const [translate_north, setTranslateNorth] = useState(false);
  const [translate_east, setTranslateEast] = useState(false);
  const [translate_south, setTranslateSouth] = useState(false);
  const [translate_west, setTranslateWest] = useState(false);
  const [translate_southEast, setTranslateSouthEast] = useState(false);
  const [translate_southWest, setTranslateSouthWest] = useState(false);
  const [translate_northEast, setTranslateNorthEast] = useState(false);
  const [translate_northWest, setTranslateNorthWest] = useState(false);
  const [attack_jumps, setAttackJumps] = useState<string[]>([]);
  const [translate_jumps, setTranslateJumps] = useState<string[]>([]);
  const [attack_slides, setAttackSlides] = useState<string[][]>([[]]);
  const [translate_slides, setTranslateSlides] = useState<string[][]>([[]]);
  const [isProgrammingAttackJumps, setIsProgrammingAttackJumps] = useState(false);
  const [isProgrammingTranslateJumps, setIsProgrammingTranslateJumps] = useState(false);
  const [isProgrammingAttackSlides, setIsProgrammingAttackSlides] = useState(false);
  const [isProgrammingTranslateSlides, setIsProgrammingTranslateSlides] = useState(false);
  const [selectedPiece, setSelectedPiece] = useState<{ piece: string | null; color: string }>({piece: 'a', color: 'black'});

  const handleDirectionChange = (direction: string, isAttack: boolean) => {
    if (isAttack) {
      switch (direction) {
        case 'north':
          setAttackNorth(!attack_north);
          break;
        case 'east':
          setAttackEast(!attack_east);
          break;
        case 'south':
          setAttackSouth(!attack_south);
          break;
        case 'west':
          setAttackWest(!attack_west);
          break;
        case 'southEast':
          setAttackSouthEast(!attack_southEast);
          break;
        case 'southWest':
          setAttackSouthWest(!attack_southWest);
          break;
        case 'northEast':
          setAttackNorthEast(!attack_northEast);
          break;
        case 'northWest':
          setAttackNorthWest(!attack_northWest);
          break;
        default:
          break;
      }
    } else {
      switch (direction) {
        case 'north':
          setTranslateNorth(!translate_north);
          break;
        case 'east':
          setTranslateEast(!translate_east);
          break;
        case 'south':
          setTranslateSouth(!translate_south);
          break;
        case 'west':
          setTranslateWest(!translate_west);
          break;
        case 'southEast':
          setTranslateSouthEast(!translate_southEast);
          break;
        case 'southWest':
          setTranslateSouthWest(!translate_southWest);
          break;
        case 'northEast':
          setTranslateNorthEast(!translate_northEast);
          break;
        case 'northWest':
          setTranslateNorthWest(!translate_northWest);
          break;
        default:
          break;
      }
    }
  };

  const handleSizeChange = (newSize: number) => {
    setSize(newSize);
  };

  const handlePieceSelect = (piece: string | null, color: string) => {
    setSelectedPiece({ piece, color });
  };

  const handleProgramAttackJumpsClick = () => {
    setIsProgrammingAttackSlides(false);
    setIsProgrammingTranslateSlides(false);
    setIsProgrammingAttackJumps(!isProgrammingAttackJumps);
  }

  const handleProgramTranslateJumpsClick = () => {
    setIsProgrammingAttackSlides(false);
    setIsProgrammingTranslateSlides(false);
    setIsProgrammingTranslateJumps(!isProgrammingTranslateJumps);
  }

  const handleProgramAttackSlidesClick = () => {
    setIsProgrammingAttackJumps(false);
    setIsProgrammingTranslateJumps(false);
    setIsProgrammingAttackSlides(!isProgrammingAttackSlides);
  }

  const handleProgramTranslateSlidesClick = () => {
    setIsProgrammingAttackJumps(false);
    setIsProgrammingTranslateJumps(false);
    setIsProgrammingTranslateSlides(!isProgrammingTranslateSlides);
  }

  const handleSquareClick = (row: number, col: number) => {
    if (isProgrammingAttackJumps) {
      const square = `${row},${col}`;
      if (attack_jumps.includes(square)) {
        setAttackJumps(attack_jumps.filter(s => s !== square));
      } else {
        setAttackJumps([...attack_jumps, square]);
      }
    } else if (isProgrammingTranslateJumps) {
      const square = `${row},${col}`;
      if (translate_jumps.includes(square)) {
        setTranslateJumps(translate_jumps.filter(s => s !== square));
      } else {
        setTranslateJumps([...translate_jumps, square]);
      }
    } else if (isProgrammingAttackSlides) {
      const square = `${row},${col}`;
      if (attack_slides[0].includes(square)) {
        setAttackSlides([attack_slides[0].filter(s => s !== square)]);
      } else {
        setAttackSlides([[...attack_slides[0], square]]);
      }
    } else if (isProgrammingTranslateSlides) {
      const square = `${row},${col}`;
      if (translate_slides[0].includes(square)) {
        setTranslateSlides([translate_slides[0].filter(s => s !== square)]);
      } else {
        setTranslateSlides([[...translate_slides[0], square]]);
      }
    }
  }

  return (
    <div className="app">
      <h1 className="app-title">Custom Piece Workshop</h1>
      <div className="main-container">
        <div className="piece-customizer-container">
          <PieceCustomizer
            size={size}
            piece={String(selectedPiece.piece)}
            attack_north={attack_north}
            attack_east={attack_east}
            attack_south={attack_south}
            attack_west={attack_west}
            attack_southEast={attack_southEast}
            attack_southWest={attack_southWest}
            attack_northEast={attack_northEast}
            attack_northWest={attack_northWest}
            translate_north={translate_north}
            translate_east={translate_east}
            translate_south={translate_south}
            translate_west={translate_west}
            translate_southEast={translate_southEast}
            translate_southWest={translate_southWest}
            translate_northEast={translate_northEast}
            translate_northWest={translate_northWest}
            attack_jumps={[]}
            translate_jumps={[]}
            attack_slides={[[]]}
            translate_slides={[[]]}
            onSquareClick={handleSquareClick}
          />
        </div>
        <PiecePanel
          size={size}
          attack_north={attack_north}
          attack_east={attack_east}
          attack_south={attack_south}
          attack_west={attack_west}
          attack_southEast={attack_southEast}
          attack_southWest={attack_southWest}
          attack_northEast={attack_northEast}
          attack_northWest={attack_northWest}
          translate_north={translate_north}
          translate_east={translate_east}
          translate_south={translate_south}
          translate_west={translate_west}
          translate_southEast={translate_southEast}
          translate_southWest={translate_southWest}
          translate_northEast={translate_northEast}
          translate_northWest={translate_northWest}
          onDirectionChange={handleDirectionChange}
          onSizeChange={handleSizeChange}
          isProgrammingAttackJumps={isProgrammingAttackJumps}
          isProgrammingTranslateJumps={isProgrammingTranslateJumps}
          isProgrammingAttackSlides={isProgrammingAttackSlides}
          isProgrammingTranslateSlides={isProgrammingTranslateSlides}
          onProgramAttackJumpsClick={handleProgramAttackJumpsClick}
          onProgramTranslateJumpsClick={handleProgramTranslateJumpsClick}
          onProgramAttackSlidesClick={handleProgramAttackSlidesClick}
          onProgramTranslateSlidesClick={handleProgramTranslateSlidesClick}
        />
      </div>
    <CustomPieceSet selectedPiece={selectedPiece} onPieceSelect={handlePieceSelect} />
    </div>
  );
}

export default App;