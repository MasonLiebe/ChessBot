import React, { useState } from 'react';
import './PiecePanel.css';
import { on } from 'events';


interface PiecePanelProps {
  size: number;
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
  onDirectionChange: (direction: string, isAttack: boolean) => void;
  onSizeChange: (size: number) => void;
  isProgrammingAttackJumps: boolean;
  isProgrammingTranslateJumps: boolean;
  isProgrammingAttackSlides: boolean;
  isProgrammingTranslateSlides: boolean;
  onProgramAttackJumpsClick: () => void;
  onProgramTranslateJumpsClick: () => void;
  onProgramAttackSlidesClick: () => void;
  onProgramTranslateSlidesClick: () => void;
  onSavePieceClick: () => void;
}

function PiecePanel({
  size,
  attack_north,
  attack_east,
  attack_south,
  attack_west,
  attack_southEast,
  attack_southWest,
  attack_northEast,
  attack_northWest,
  translate_north,
  translate_east,
  translate_south,
  translate_west,
  translate_southEast,
  translate_southWest,
  translate_northEast,
  translate_northWest,
  onDirectionChange,
  onSizeChange,
  isProgrammingAttackJumps,
  isProgrammingTranslateJumps,
  isProgrammingAttackSlides,
  isProgrammingTranslateSlides,
  onProgramAttackJumpsClick,
  onProgramTranslateJumpsClick,
  onProgramAttackSlidesClick,
  onProgramTranslateSlidesClick,
  onSavePieceClick,
}: PiecePanelProps) {
  const handleDirectionClick = (direction: string, isAttack: boolean) => {
    onDirectionChange(direction, isAttack);
  };

  const handleSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newSize = parseInt(event.target.value);
    onSizeChange(newSize);
  };

  return (
    <div className="piece-panel">
      <div className="direction-grid">
      <div className="row">
        <div className="row-label"></div>
        <div className="column-labels">
          <div>Attack</div>
        </div>
        <div className="column-labels">
          <div>Translate</div>
        </div>
      </div>
        <div className="direction-rows">
          <div className="row">
            <div className="row-label">North</div>
            <button
              className={attack_north ? 'active' : ''}
              onClick={() => handleDirectionClick('north', true)}
            ></button>
            <button
              className={translate_north ? 'active' : ''}
              onClick={() => handleDirectionClick('north', false)}
            ></button>
          </div>
          <div className="row">
            <div className="row-label">East</div>
            <button
              className={attack_east ? 'active' : ''}
              onClick={() => handleDirectionClick('east', true)}
            ></button>
            <button
              className={translate_east ? 'active' : ''}
              onClick={() => handleDirectionClick('east', false)}
            ></button>
          </div>
          <div className="row">
            <div className="row-label">South</div>
            <button
              className={attack_south ? 'active' : ''}
              onClick={() => handleDirectionClick('south', true)}
            ></button>
            <button
              className={translate_south ? 'active' : ''}
              onClick={() => handleDirectionClick('south', false)}
            ></button>
          </div>
          <div className="row">
            <div className="row-label">West</div>
            <button
              className={attack_west ? 'active' : ''}
              onClick={() => handleDirectionClick('west', true)}
            ></button>
            <button
              className={translate_west ? 'active' : ''}
              onClick={() => handleDirectionClick('west', false)}
            ></button>
          </div>
          <div className="row">
            <div className="row-label">South-East</div>
            <button
              className={attack_southEast ? 'active' : ''}
              onClick={() => handleDirectionClick('southEast', true)}
            ></button>
            <button
              className={translate_southEast ? 'active' : ''}
              onClick={() => handleDirectionClick('southEast', false)}
            ></button>
          </div>
          <div className="row">
            <div className="row-label">South-West</div>
            <button
              className={attack_southWest ? 'active' : ''}
              onClick={() => handleDirectionClick('southWest', true)}
            ></button>
            <button
              className={translate_southWest ? 'active' : ''}
              onClick={() => handleDirectionClick('southWest', false)}
            ></button>
          </div>
          <div className="row">
            <div className="row-label">North-East</div>
            <button
              className={attack_northEast ? 'active' : ''}
              onClick={() => handleDirectionClick('northEast', true)}
            ></button>
            <button
              className={translate_northEast ? 'active' : ''}
              onClick={() => handleDirectionClick('northEast', false)}
            ></button>
          </div>
          <div className="row">
            <div className="row-label">North-West</div>
            <button
              className={attack_northWest ? 'active' : ''}
              onClick={() => handleDirectionClick('northWest', true)}
            ></button>
            <button
              className={translate_northWest ? 'active' : ''}
              onClick={() => handleDirectionClick('northWest', false)}
            ></button>
          </div>
        </div>
      </div>
      <div className="program-buttons">
        <button
          className={isProgrammingAttackJumps ? 'active-attack' : ''}
          onClick={onProgramAttackJumpsClick}
        >
          Program Attack Jumps
        </button>
        <button
          className={isProgrammingTranslateJumps ? 'active-translate' : ''}
          onClick={onProgramTranslateJumpsClick}
        >
          Program Translate Jumps
        </button>
        <button
          className={isProgrammingAttackSlides ? 'active-attack' : ''}
          onClick={onProgramAttackSlidesClick}
        >
          Program Attack Slides
        </button>
        <button
          className={isProgrammingTranslateSlides ? 'active-translate' : ''}
          onClick={onProgramTranslateSlidesClick}
        >
          Program Translate Slides
        </button>
      </div>
      <button className="save-piece" onClick={onSavePieceClick}>
        Save Piece
      </button>
      <div className="size-slider">
        <label htmlFor="size">Board Size: {size}</label>
        <input
          id="size"
          type="range"
          min="5"
          max="31"
          step="2"
          value={size}
          onChange={handleSizeChange}
        />
      </div>

    </div>
  );
}

export default PiecePanel;