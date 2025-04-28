import React, { ReactElement } from 'react';
import './CardGrid.css';

interface CardGridProps<T> {
  data: T[];
  renderItem: (item: T, index: number) => ReactElement;
  gridHeight?: string;
  gridWidth?: string;
  columnCount?: number;
}

const CardGrid = <T extends object>({
  data,
  renderItem,
  gridHeight = '500px',
  gridWidth = '100%',
  columnCount = 3
}: CardGridProps<T>) => {
  return (
    <div 
      className="card-grid-container"
      style={{ 
        height: gridHeight, 
        width: gridWidth 
      }}
    >
      <div 
        className="card-grid" 
        style={{ 
          gridTemplateColumns: `repeat(${columnCount}, 1fr)` 
        }}
      >
        {data.map((item, index) => (
          <div key={index} className="card-grid-item">
            {renderItem(item, index)}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CardGrid;
