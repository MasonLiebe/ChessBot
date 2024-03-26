import React from 'react';
import './BoardPanel.css';

interface BoardPanelProps {
  rows: number;
  columns: number;
  isSquare: boolean;
  onRowsChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onColumnsChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onSquareToggle: () => void;
}

function BoardPanel({
  rows,
  columns,
  isSquare,
  onRowsChange,
  onColumnsChange,
  onSquareToggle,
}: BoardPanelProps) {
  return (
    <div className="board-panel">
      <div className="slider">
        <label htmlFor="rows-slider">Rows: {rows}</label>
        <input
          id="rows-slider"
          type="range"
          min="1"
          max="16"
          value={rows}
          onChange={onRowsChange}
        />
      </div>
      <div className="slider">
        <label htmlFor="columns-slider">Columns: {columns}</label>
        <input
          id="columns-slider"
          type="range"
          min="1"
          max="16"
          value={columns}
          onChange={onColumnsChange}
        />
      </div>
      <div className="toggle-container">
        <label htmlFor="square-toggle">Lock as Square:</label>
        <input
          id="square-toggle"
          type="checkbox"
          checked={isSquare}
          onChange={onSquareToggle}
        />
      </div>
    </div>
  );
}

export default BoardPanel;