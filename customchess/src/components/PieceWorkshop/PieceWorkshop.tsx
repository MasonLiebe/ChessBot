import React, { useState } from 'react';
import './PieceWorkshop.css';
import PieceCustomizer from '../PieceCustomizer/PieceCustomizer';
import PiecePanel from '../PiecePanel/PiecePanel';
import CustomPieceSet from '../CustomPIeceSet/CustomPieceSet';

export function PieceWorkshop() {
  
  const [size, setSize] = useState(15);
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

  const [movementPatterns, setMovementPatterns] = useState<MovementPattern[]>([
    patternA,
    patternB,
    patternC,
    patternD,
    patternE,
    patternF,
  ]);

  const [selectedPattern, setSelectedPattern] = useState<MovementPattern>(patternA);

  let [activePatternIndex, setActivePatternIndex] = useState(0);

  const handleDirectionChange = (direction: string, isAttack: boolean) => {
    setSelectedPattern((prevPattern) => ({
      ...prevPattern,
      [`${isAttack ? 'attack' : 'translate'}_${direction}`]: !prevPattern[`${isAttack ? 'attack' : 'translate'}_${direction}` as keyof MovementPattern],
    }));
  };

  const handleSizeChange = (newSize: number) => {
    setSize(newSize);
  };

  const handlePieceSelect = (piece: string | null, color: string) => {
    console.log(piece, color);
    setSelectedPiece({ piece, color });
    if (piece === 'a') {
      setSelectedPattern(movementPatterns[0]);
      setActivePatternIndex(0);
    }
    if (piece === 'c') {
      setSelectedPattern(movementPatterns[1]);
      setActivePatternIndex(1);
    }
    if (piece === 'd') {
      setSelectedPattern(movementPatterns[2]);
      setActivePatternIndex(2);
    }
    if (piece === 'e') {
      setSelectedPattern(movementPatterns[3]);
      setActivePatternIndex(3);
    }
    if (piece === 'f') {
      setSelectedPattern(movementPatterns[4]);
      setActivePatternIndex(4);
    }
    if (piece === 'g') {
      setSelectedPattern(movementPatterns[5]);
      setActivePatternIndex(5);
    }
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

  const handleClearPatternClick = () => {
    setSelectedPattern({
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
      attack_jumps: [],
      translate_jumps: [],
      attack_slides: [],
      translate_slides: [],
    });
  }

  const handleDefaultPatternClick = () => {
    // sets the default pattern for the selected piece
    if (selectedPiece.piece === 'a') {
      setSelectedPattern(patternA);
    }
    if (selectedPiece.piece === 'c') {
      setSelectedPattern(patternB);
    }
    if (selectedPiece.piece === 'd') {
      setSelectedPattern(patternC);
    }
    if (selectedPiece.piece === 'e') {
      setSelectedPattern(patternD);
    }
    if (selectedPiece.piece === 'f') {
      setSelectedPattern(patternE);
    }
    if (selectedPiece.piece === 'g') {
      setSelectedPattern(patternF);
    }
  }

  const handleProgramTranslateSlidesClick = () => {
    setIsProgrammingAttackJumps(false);
    setIsProgrammingTranslateJumps(false);
    setIsProgrammingTranslateSlides(!isProgrammingTranslateSlides);
  }

  const handleSavePieceClick = () => {
    const updatedMovementPatterns = [...movementPatterns];
    updatedMovementPatterns[activePatternIndex] = selectedPattern;
    setMovementPatterns(updatedMovementPatterns);
    console.log(movementPatterns[activePatternIndex]);
  };

  const toggleJump = (jumps: [number, number][], jumpCoord: [number, number]): [number, number][] => {
    const index = jumps.findIndex(
      (jump) => jump[0] === jumpCoord[0] && jump[1] === jumpCoord[1]
    );
  
    if (index !== -1) {
      return jumps.filter((_, i) => i !== index);
    } else {
      return [...jumps, jumpCoord];
    }
  };
  
  function toggleSlide(attack_slides: [number, number][][], arg1: number[]): [number, number][][] {
    throw new Error('Function not implemented.');
  }

  const handleSquareClick = (row: number, col: number) => {
    if (isProgrammingAttackJumps) {
      setSelectedPattern((prevPattern) => ({
        ...prevPattern,
        attack_jumps: toggleJump(prevPattern.attack_jumps, [row, col]),
      }));
    }
    if (isProgrammingTranslateJumps) {
      setSelectedPattern((prevPattern) => ({
        ...prevPattern,
        translate_jumps: toggleJump(prevPattern.translate_jumps, [row, col]),
      }));
    }
    if (isProgrammingAttackSlides) {
      setSelectedPattern((prevPattern) => ({
        ...prevPattern,
        attack_slides: toggleSlide(prevPattern.attack_slides, [row, col]),
      }));
    }
    if (isProgrammingTranslateSlides) {
      setSelectedPattern((prevPattern) => ({
        ...prevPattern,
        translate_slides: toggleSlide(prevPattern.translate_slides, [row, col]),
      }));
    }
  };

  return (
    <div className="app">
      <div className="main-container-piece">
        <div className="chessboard-wrapper-piece">
          <div className="chessboard-container-piece">
            <PieceCustomizer
              size={size}
              piece={String(selectedPiece.piece)}
              attack_north={selectedPattern.attack_north}
              attack_east={selectedPattern.attack_east}
              attack_west={selectedPattern.attack_west}
              attack_south={selectedPattern.attack_south}
              attack_southEast={selectedPattern.attack_southEast}
              attack_southWest={selectedPattern.attack_southWest}
              attack_northEast={selectedPattern.attack_northEast}
              attack_northWest={selectedPattern.attack_northWest}
              translate_north={selectedPattern.translate_north}
              translate_east={selectedPattern.translate_east}
              translate_south={selectedPattern.translate_south}
              translate_west={selectedPattern.translate_west}
              translate_southEast={selectedPattern.translate_southEast}
              translate_southWest={selectedPattern.translate_southWest}
              translate_northEast={selectedPattern.translate_northEast}
              translate_northWest={selectedPattern.translate_northWest}
              attack_jumps={selectedPattern.attack_jumps}
              translate_jumps={selectedPattern.translate_jumps}
              attack_slides={[[]]}
              translate_slides={[[]]}
              onSquareClick={handleSquareClick}
            />
            <CustomPieceSet selectedPiece={selectedPiece} onPieceSelect={handlePieceSelect} />
          </div>
        </div>
        <PiecePanel
          size={size}
          attack_north={selectedPattern.attack_north}
          attack_east={selectedPattern.attack_east}
          attack_west={selectedPattern.attack_west}
          attack_south={selectedPattern.attack_south}
          attack_southEast={selectedPattern.attack_southEast}
          attack_southWest={selectedPattern.attack_southWest}
          attack_northEast={selectedPattern.attack_northEast}
          attack_northWest={selectedPattern.attack_northWest}
          translate_north={selectedPattern.translate_north}
          translate_east={selectedPattern.translate_east}
          translate_south={selectedPattern.translate_south}
          translate_west={selectedPattern.translate_west}
          translate_southEast={selectedPattern.translate_southEast}
          translate_southWest={selectedPattern.translate_southWest}
          translate_northEast={selectedPattern.translate_northEast}
          translate_northWest={selectedPattern.translate_northWest}
          onDirectionChange={handleDirectionChange}
          onSizeChange={handleSizeChange}
          isProgrammingAttackJumps={isProgrammingAttackJumps}
          isProgrammingTranslateJumps={isProgrammingTranslateJumps}
          isProgrammingAttackSlides={isProgrammingAttackSlides}
          isProgrammingTranslateSlides={isProgrammingTranslateSlides}
          onProgramAttackJumpsClick={handleProgramAttackJumpsClick}
          onProgramTranslateJumpsClick={handleProgramTranslateJumpsClick}
          onClearPatternClick={handleClearPatternClick}
          onDefaultPatternClick={handleDefaultPatternClick}
          onSavePieceClick={handleSavePieceClick}
        />
      </div>
    </div>
  );
}