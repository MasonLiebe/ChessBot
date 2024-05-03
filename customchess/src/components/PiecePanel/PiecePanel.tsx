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
  onClearPatternClick: () => void;
  onDefaultPatternClick: () => void;
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
  onClearPatternClick,
  onDefaultPatternClick,
  onSavePieceClick,
}: PiecePanelProps) {
  const handleDirectionClick = (direction: string, isAttack: boolean) => {
    onDirectionChange(direction, isAttack);
  };

  const handleSizeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newSize = parseInt(event.target.value);
    onSizeChange(newSize);
  };

  function getIconClass(direction: string) {
    let attackActive = false;
    let translateActive = false;
  
    switch (direction) {
      case 'north':
        attackActive = attack_north;
        translateActive = translate_north;
        break;
      case 'east':
        attackActive = attack_east;
        translateActive = translate_east;
        break;
      case 'south':
        attackActive = attack_south;
        translateActive = translate_south;
        break;
      case 'west':
        attackActive = attack_west;
        translateActive = translate_west;
        break;
      case 'southEast':
        attackActive = attack_southEast;
        translateActive = translate_southEast;
        break;
      case 'southWest':
        attackActive = attack_southWest;
        translateActive = translate_southWest;
        break;
      case 'northEast':
        attackActive = attack_northEast;
        translateActive = translate_northEast;
        break;
      case 'northWest':
        attackActive = attack_northWest;
        translateActive = translate_northWest;
        break;
      default:
        break;
    }
  
    if (attackActive && translateActive) {
      return 'both';
    } else if (attackActive) {
      return 'attack';
    } else if (translateActive) {
      return 'translate';
    } else {
      return 'none';
    }
  }

  return (
    <div className="piece-panel">
      <table className="direction-grid">
        <thead>
          <tr>
            <th></th>
            <th>Attack</th>
            <th>Translate</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="row-label">
              <img src="/assets/arrows/up-gold.svg" alt='up' className={getIconClass('north')} />
            </td>
            <td>
              <button
                className={attack_north ? 'active' : ''}
                onClick={() => handleDirectionClick('north', true)}
              ></button>
            </td>
            <td>
              <button
                className={translate_north ? 'active' : ''}
                onClick={() => handleDirectionClick('north', false)}
              ></button>
            </td>
          </tr>
          <tr>
            <td className="row-label">
              <img src="/assets/arrows/right-gold.svg" alt="Right" className={getIconClass('east')} />
            </td>
            <td>
              <button
                className={attack_east ? 'active' : ''}
                onClick={() => handleDirectionClick('east', true)}
              ></button>
            </td>
            <td>
              <button
                className={translate_east ? 'active' : ''}
                onClick={() => handleDirectionClick('east', false)}
              ></button>
            </td>
          </tr>
          <tr>
            <td className="row-label">
              <img src="/assets/arrows/down-gold.svg" alt="Down" className={getIconClass('south')} />
            </td>
            <td>
              <button
                className={attack_south ? 'active' : ''}
                onClick={() => handleDirectionClick('south', true)}
              ></button>
            </td>
            <td>
              <button
                className={translate_south ? 'active' : ''}
                onClick={() => handleDirectionClick('south', false)}
              ></button>
            </td>
          </tr>
          <tr>
            <td className="row-label">
              <img src="/assets/arrows/left-gold.svg" alt="Left" className={getIconClass('west')} />
            </td>
            <td>
              <button
                className={attack_west ? 'active' : ''}
                onClick={() => handleDirectionClick('west', true)}
              ></button>
            </td>
            <td>
              <button
                className={translate_west ? 'active' : ''}
                onClick={() => handleDirectionClick('west', false)}
              ></button>
            </td>
          </tr>
          <tr>
            <td className="row-label">
              <img src="/assets/arrows/down-right-gold.svg" alt="Down-Right" className={getIconClass('southEast')} />
            </td>
            <td>
              <button
                className={attack_southEast ? 'active' : ''}
                onClick={() => handleDirectionClick('southEast', true) }
              ></button>
            </td>
            <td>
              <button
                className={translate_southEast ? 'active' : ''}
                onClick={() => handleDirectionClick('southEast', false)}
              ></button>
            </td>
          </tr>
          <tr>
            <td className="row-label">
              <img src="/assets/arrows/down-left-gold.svg" alt="Down-Left" className={getIconClass('southWest')} />
            </td>
            <td>
              <button
                className={attack_southWest ? 'active' : ''}
                onClick={() => handleDirectionClick('southWest', true)}
              ></button>
            </td>
            <td>
              <button
                className={translate_southWest ? 'active' : ''}
                onClick={() => handleDirectionClick('southWest', false)}
              ></button>
            </td>
          </tr>
          <tr>
            <td className="row-label">
              <img src="/assets/arrows/up-right-gold.svg" alt="Up-Right" className={getIconClass('northEast')} />
            </td>
            <td>
              <button
                className={attack_northEast ? 'active' : ''}
                onClick={() => handleDirectionClick('northEast', true)}
              ></button>
            </td>
            <td>
              <button
                className={translate_northEast ? 'active' : ''}
                onClick={() => handleDirectionClick('northEast', false)}
              ></button>
            </td>
          </tr>
          <tr>
            <td className="row-label">
              <img src="/assets/arrows/up-left-gold.svg" alt="Up-Left" className={getIconClass('northWest')} />
            </td>
            <td>
              <button
                className={attack_northWest ? 'active' : ''}
                onClick={() => handleDirectionClick('northWest', true)}
              ></button>
            </td>
            <td>
              <button
                className={translate_northWest ? 'active' : ''}
                onClick={() => handleDirectionClick('northWest', false)}
              ></button>
            </td>
          </tr>
        </tbody>
      </table>
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
          onClick={onClearPatternClick}
        >
          Clear Pattern
        </button>
        <button
          onClick={onDefaultPatternClick}
        >
          Set to Default Pattern
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