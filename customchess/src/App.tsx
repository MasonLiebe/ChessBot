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
  const [attack_jumps, setAttackJumps] = useState<[number, number][]>([[-4, 0], [-4, 2], [-4, -2], [-2, 0], [-2, 2], [-2, -2], [-2, 4], [-2, -4], [-3, 1], [-3, 3], [-3, -1], [-3, -3], [-1, 1], [-1, 3], [-1, -1], [-1, -3], [0, 4], [0, -4], [0, 2], [0, -2], [1, 1], [1, 3], [1, -1], [1, -3], [3, 1], [3, 3], [3, -1], [3, -3], [4, 0], [4, 2], [4, -2], [2, 0], [2, 2], [2, -2], [2, -4], [2, 4]]);
  const [translate_jumps, setTranslateJumps] = useState<[number, number][]>([[-4, 0], [-4, 2], [-4, -2], [-2, 0], [-2, 2], [-2, -2], [-2, 4], [-2, -4], [-3, 1], [-3, 3], [-3, -1], [-3, -3], [-1, 1], [-1, 3], [-1, -1], [-1, -3], [0, 4], [0, -4], [0, 2], [0, -2], [1, 1], [1, 3], [1, -1], [1, -3], [3, 1], [3, 3], [3, -1], [3, -3], [4, 0], [4, 2], [4, -2], [2, 0], [2, 2], [2, -2], [2, -4], [2, 4]]);
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

  let movementPatterns = [] as MovementPattern[];

  let patternA: MovementPattern = {
    attack_north: false,
    attack_east: false,
    attack_south: false,
    attack_west: false,
    attack_southEast: false,
    attack_southWest: false,
    attack_northEast: false,
    attack_northWest: false,
    translate_north: false,
    translate_east: false,
    translate_south: false,
    translate_west: false,
    translate_southEast: false,
    translate_southWest: false,
    translate_northEast: false,
    translate_northWest: false,
    attack_jumps: [[-4, 0], [-4, 2], [-4, -2], [-2, 0], [-2, 2], [-2, -2], [-2, 4], [-2, -4], [-3, 1], [-3, 3], [-3, -1], [-3, -3], [-1, 1], [-1, 3], [-1, -1], [-1, -3], [0, 4], [0, -4], [0, 2], [0, -2], [1, 1], [1, 3], [1, -1], [1, -3], [3, 1], [3, 3], [3, -1], [3, -3], [4, 0], [4, 2], [4, -2], [2, 0], [2, 2], [2, -2], [2, -4], [2, 4]],
    translate_jumps: [[-4, 0], [-4, 2], [-4, -2], [-2, 0], [-2, 2], [-2, -2], [-2, 4], [-2, -4], [-3, 1], [-3, 3], [-3, -1], [-3, -3], [-1, 1], [-1, 3], [-1, -1], [-1, -3], [0, 4], [0, -4], [0, 2], [0, -2], [1, 1], [1, 3], [1, -1], [1, -3], [3, 1], [3, 3], [3, -1], [3, -3], [4, 0], [4, 2], [4, -2], [2, 0], [2, 2], [2, -2],[2, -4], [2, 4]],
    attack_slides: [],
    translate_slides: [],
  };

  let patternB: MovementPattern = {
    attack_north: false,
    attack_east: false,
    attack_south: false,
    attack_west: false,
    attack_southEast: false,
    attack_southWest: false,
    attack_northEast: false,
    attack_northWest: false,
    translate_north: false,
    translate_east: false,
    translate_south: false,
    translate_west: false,
    translate_southEast: false,
    translate_southWest: false,
    translate_northEast: false,
    translate_northWest: false,
    attack_jumps: [[-2, 2], [-2, 1], [-2, 0],[-2,-1], [-2, -2], [-1, 2], [-1, 1], [-1, 0], [-1, -1], [-1, -2], [0, 2], [0, 1], [0, -1], [0, -2], [1, 2], [1, 1], [1, 0], [1, -1], [1, -2], [2, 2], [2, 1], [2, 0], [2, -1], [2, -2]],
    translate_jumps: [[-2, 2], [-2, 1], [-2, 0],[-2,-1], [-2, -2], [-1, 2], [-1, 1], [-1, 0], [-1, -1], [-1, -2], [0, 2], [0, 1], [0, -1], [0, -2], [1, 2], [1, 1], [1, 0], [1, -1], [1, -2], [2, 2], [2, 1], [2, 0], [2, -1], [2, -2]],
    attack_slides: [],
    translate_slides: [],
  };

  let patternC: MovementPattern = {
    attack_north: true,
    attack_east: true,
    attack_south: true,
    attack_west: true,
    attack_southEast: true,
    attack_southWest: true,
    attack_northEast: true,
    attack_northWest: true,
    translate_north: true,
    translate_east: true,
    translate_south: true,
    translate_west: true,
    translate_southEast: true,
    translate_southWest: true,
    translate_northEast: true,
    translate_northWest: true,
    attack_jumps: [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]],
    translate_jumps: [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]],
    attack_slides: [],
    translate_slides: [],
  };

  let patternD: MovementPattern = {
    attack_north: true,
    attack_east: true,
    attack_south: true,
    attack_west: true,
    attack_southEast: true,
    attack_southWest: true,
    attack_northEast: true,
    attack_northWest: true,
    translate_north: true,
    translate_east: true,
    translate_south: false,
    translate_west: true,
    translate_southEast: false,
    translate_southWest: false,
    translate_northEast: true,
    translate_northWest: true,
    attack_jumps: [],
    translate_jumps: [],
    attack_slides: [],
    translate_slides: [],
  };

  let patternE: MovementPattern = {
    attack_north: true,
    attack_east: true,
    attack_south: true,
    attack_west: true,
    attack_southEast: false,
    attack_southWest: false,
    attack_northEast: false,
    attack_northWest: false,
    translate_north: true,
    translate_east: true,
    translate_south: true,
    translate_west: true,
    translate_southEast: false,
    translate_southWest: false,
    translate_northEast: false,
    translate_northWest: false,
    attack_jumps: [[3, 4], [3, -4], [4, 3], [4, -3], [-3, 4], [-3, -4], [-4, 3], [-4, -3], [5, 12], [5, -12], [12, 5], [12, -5], [-5, 12], [-5, -12], [-12, 5], [-12, -5]],
    translate_jumps: [[3, 4], [3, -4], [4, 3], [4, -3], [-3, 4], [-3, -4], [-4, 3], [-4, -3], [5, 12], [5, -12], [12, 5], [12, -5], [-5, 12], [-5, -12], [-12, 5], [-12, -5]],
    attack_slides: [],
    translate_slides: [],
  };

  let patternF: MovementPattern = {
    attack_north: true,
    attack_east: true,
    attack_south: true,
    attack_west: true,
    attack_southEast: false,
    attack_southWest: false,
    attack_northEast: false,
    attack_northWest: false,
    translate_north: true,
    translate_east: true,
    translate_south: true,
    translate_west: true,
    translate_southEast: false,
    translate_southWest: false,
    translate_northEast: false,
    translate_northWest: false,
    attack_jumps: [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]],
    translate_jumps: [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]],
    attack_slides: [],
    translate_slides: [],
  };

  movementPatterns.push(patternA, patternB, patternC, patternD, patternE, patternF);

  let activePatternIndex = 0;

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
    console.log(piece, color);
    setSelectedPiece({ piece, color });
    if (piece === 'a') {
      activePatternIndex = 0;
    }
    if (piece === 'c') {
      activePatternIndex = 1;
    }
    if (piece === 'd') {
      activePatternIndex = 2;
    }
    if (piece === 'e') {
      activePatternIndex = 3;
    }
    if (piece === 'f') {
      activePatternIndex = 4;
    }
    if (piece === 'g') {
      activePatternIndex = 5;
    }

    setAttackNorth(movementPatterns[activePatternIndex].attack_north);
    setAttackEast(movementPatterns[activePatternIndex].attack_east);
    setAttackSouth(movementPatterns[activePatternIndex].attack_south);
    setAttackWest(movementPatterns[activePatternIndex].attack_west);
    setAttackSouthEast(movementPatterns[activePatternIndex].attack_southEast);
    setAttackSouthWest(movementPatterns[activePatternIndex].attack_southWest);
    setAttackNorthEast(movementPatterns[activePatternIndex].attack_northEast);
    setAttackNorthWest(movementPatterns[activePatternIndex].attack_northWest);
    setTranslateNorth(movementPatterns[activePatternIndex].translate_north);
    setTranslateEast(movementPatterns[activePatternIndex].translate_east);
    setTranslateSouth(movementPatterns[activePatternIndex].translate_south);
    setTranslateWest(movementPatterns[activePatternIndex].translate_west);
    setTranslateSouthEast(movementPatterns[activePatternIndex].translate_southEast);
    setTranslateSouthWest(movementPatterns[activePatternIndex].translate_southWest);
    setTranslateNorthEast(movementPatterns[activePatternIndex].translate_northEast);
    setTranslateNorthWest(movementPatterns[activePatternIndex].translate_northWest);
    setAttackJumps(movementPatterns[activePatternIndex].attack_jumps);
    setTranslateJumps(movementPatterns[activePatternIndex].translate_jumps);
    setAttackSlides(movementPatterns[activePatternIndex].attack_slides);
    setTranslateSlides(movementPatterns[activePatternIndex].translate_slides);
    console.log(movementPatterns[activePatternIndex].attack_north);
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

  const handleSavePieceClick = () => {
    movementPatterns[activePatternIndex].attack_north = attack_north;
    movementPatterns[activePatternIndex].attack_east = attack_east;
    movementPatterns[activePatternIndex].attack_south = attack_south;
    movementPatterns[activePatternIndex].attack_west = attack_west;
    movementPatterns[activePatternIndex].attack_southEast = attack_southEast;
    movementPatterns[activePatternIndex].attack_southWest = attack_southWest;
    movementPatterns[activePatternIndex].attack_northEast = attack_northEast;
    movementPatterns[activePatternIndex].attack_northWest = attack_northWest;
    movementPatterns[activePatternIndex].translate_north = translate_north;
    movementPatterns[activePatternIndex].translate_east = translate_east;
    movementPatterns[activePatternIndex].translate_south = translate_south;
    movementPatterns[activePatternIndex].translate_west = translate_west;
    movementPatterns[activePatternIndex].translate_southEast = translate_southEast;
    movementPatterns[activePatternIndex].translate_southWest = translate_southWest;
    movementPatterns[activePatternIndex].translate_northEast = translate_northEast;
    movementPatterns[activePatternIndex].translate_northWest = translate_northWest;
    movementPatterns[activePatternIndex].attack_jumps = attack_jumps;
    movementPatterns[activePatternIndex].translate_jumps = translate_jumps;
    movementPatterns[activePatternIndex].attack_slides = attack_slides;
    movementPatterns[activePatternIndex].translate_slides = translate_slides;
    console.log(movementPatterns[0].attack_north);
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
    console.log(attack_jumps);
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
          onSavePieceClick={handleSavePieceClick}
        />
      </div>
    </div>
  );
}

export default App;