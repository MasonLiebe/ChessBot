import React, { useState } from 'react';
import './PieceWorkshop.css';
import PieceCustomizer from '../PieceCustomizer/PieceCustomizer';
import PiecePanel from '../PiecePanel/PiecePanel';
import CustomPieceSet from '../CustomPIeceSet/CustomPieceSet';
import { DefaultCustomPatterns, MovementPattern } from '../MovementPattern';

interface PieceWorkshopProps {
  sendPiece: () => void;
}

function PieceWorkshop({sendPiece}: PieceWorkshopProps) {
  
  const [size, setSize] = useState(15);
  const [isProgrammingAttackJumps, setIsProgrammingAttackJumps] = useState(false);
  const [isProgrammingTranslateJumps, setIsProgrammingTranslateJumps] = useState(false);
  const [isProgrammingAttackSlides, setIsProgrammingAttackSlides] = useState(false);
  const [isProgrammingTranslateSlides, setIsProgrammingTranslateSlides] = useState(false);
  const [selectedPiece, setSelectedPiece] = useState<{ piece: string | null; color: string }>({piece: 'a', color: 'black'});

  const [movementPatterns, setMovementPatterns] = useState<MovementPattern[]>(DefaultCustomPatterns);

  const [selectedPattern, setSelectedPattern] = useState<MovementPattern>(movementPatterns[0]);

  let [activePatternIndex, setActivePatternIndex] = useState(0);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);


  const handleDirectionChange = (direction: string, isAttack: boolean) => {
    setSelectedPattern((prevPattern) => ({
      ...prevPattern,
      [`${isAttack ? 'attack' : 'translate'}_${direction}`]: !prevPattern[`${isAttack ? 'attack' : 'translate'}_${direction}` as keyof MovementPattern],
    }));
    setHasUnsavedChanges(true);
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
    setHasUnsavedChanges(false);
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
    setHasUnsavedChanges(true);
  }

  const handleDefaultPatternClick = () => {
    // sets the default pattern for the selected piece
    if (selectedPiece.piece === 'a') {
      setSelectedPattern(movementPatterns[0]);
    }
    if (selectedPiece.piece === 'c') {
      setSelectedPattern(movementPatterns[1]);
    }
    if (selectedPiece.piece === 'd') {
      setSelectedPattern(movementPatterns[2]);
    }
    if (selectedPiece.piece === 'e') {
      setSelectedPattern(movementPatterns[3]);
    }
    if (selectedPiece.piece === 'f') {
      setSelectedPattern(movementPatterns[4]);
    }
    if (selectedPiece.piece === 'g') {
      setSelectedPattern(movementPatterns[5]);
    }
    setHasUnsavedChanges(true);
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
    setHasUnsavedChanges(false);
  };

  const toggleJump = (jumps: [number, number][], jumpCoord: [number, number]): [number, number][] => {
    const index = jumps.findIndex(
      (jump) => jump[0] === jumpCoord[0] && jump[1] === jumpCoord[1]
    );
    setHasUnsavedChanges(true);
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
        <div className="chessboard-wrapper-piece">`
          <div className="chessboard-container-piece">
          <div className={`changes-message`}>
              {hasUnsavedChanges ? 'Warning! Unsaved Changes' : 'Piece Saved!'}
          </div>
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

export {PieceWorkshop};