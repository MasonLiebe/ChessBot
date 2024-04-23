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
  const [attack_jumps, setAttackJumps] = useState<[number, number][]>([]);
  const [translate_jumps, setTranslateJumps] = useState<[number, number][]>([]);
  const [attack_slides, setAttackSlides] = useState<[number, number][][]>([]);
  const [translate_slides, setTranslateSlides] = useState<[number, number][][]>([]);
  const [isProgrammingAttackJumps, setIsProgrammingAttackJumps] = useState(false);
  const [isProgrammingTranslateJumps, setIsProgrammingTranslateJumps] = useState(false);
  const [isProgrammingAttackSlides, setIsProgrammingAttackSlides] = useState(false);
  const [isProgrammingTranslateSlides, setIsProgrammingTranslateSlides] = useState(false);
  const [selectedPiece, setSelectedPiece] = useState<{ piece: string | null; color: string }>({piece: 'a', color: 'black'});

  interface MovementPattern {
    attack_north: boolean;
    attack_east: boolean;
    attack_south: boolean;
    attack_west: boolean;
    attack_southEast: boolean;
    attack_southWest: boolean;
    attack_northEast: boolean;
    attack_northWest: boolean;
    translate_north: boolean;
    translate_east: boolean;
    translate_south: boolean;
    translate_west: boolean;
    translate_southEast: boolean;
    translate_southWest: boolean;
    translate_northEast: boolean;
    translate_northWest: boolean;
    attack_jumps: [number, number][];
    translate_jumps: [number, number][];
    attack_slides: [number, number][][];
    translate_slides: [number, number][][];
  }

  const movementPatterns: Record<string, MovementPattern> = {};

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
      const jumpCoord: [number, number] = [row, col];
      const index = attack_jumps.findIndex(
        jump => jump[0] === jumpCoord[0] && jump[1] === jumpCoord[1]
      );
  
      if (index !== -1) {
        setAttackJumps(attack_jumps.filter((_, i) => i !== index));
      } else {
        setAttackJumps([...attack_jumps, jumpCoord]);
      }
    } 
    if (isProgrammingTranslateJumps) {
      const jumpCoord: [number, number] = [row, col];
      const index = translate_jumps.findIndex(
        jump => jump[0] === jumpCoord[0] && jump[1] === jumpCoord[1]
      );
  
      if (index !== -1) {
        setTranslateJumps(translate_jumps.filter((_, i) => i !== index));
      } else {
        setTranslateJumps([...translate_jumps, jumpCoord]);
      }
    }
    if (isProgrammingAttackSlides) {
      const slideCoord: [number, number] = [row, col];
      const slideIndex = attack_slides.findIndex(slide =>
        slide.some(coord => coord[0] === slideCoord[0] && coord[1] === slideCoord[1])
      );
  
      if (slideIndex !== -1) {
        const updatedSlides = attack_slides.map((slide, i) =>
          i === slideIndex ? slide.filter(coord => coord[0] !== slideCoord[0] || coord[1] !== slideCoord[1]) : slide
        );
        setAttackSlides(updatedSlides.filter(slide => slide.length > 0));
      } else {
        setAttackSlides([...attack_slides, [slideCoord]]);
      }
    } 
    if (isProgrammingTranslateSlides) {
      const slideCoord: [number, number] = [row, col];
      const slideIndex = translate_slides.findIndex(slide =>
        slide.some(coord => coord[0] === slideCoord[0] && coord[1] === slideCoord[1])
      );
  
      if (slideIndex !== -1) {
        const updatedSlides = translate_slides.map((slide, i) =>
          i === slideIndex ? slide.filter(coord => coord[0] !== slideCoord[0] || coord[1] !== slideCoord[1]) : slide
        );
        setTranslateSlides(updatedSlides.filter(slide => slide.length > 0));
      } else {
        setTranslateSlides([...translate_slides, [slideCoord]]);
      }
    }
  };

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
            attack_jumps={attack_jumps}
            translate_jumps={translate_jumps}
            attack_slides={[[]]}
            translate_slides={[[]]}
            onSquareClick={handleSquareClick}
          />
          <CustomPieceSet selectedPiece={selectedPiece} onPieceSelect={handlePieceSelect} />
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
    </div>
  );
}

export default App;