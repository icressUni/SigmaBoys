import React from 'react';
import './DropdownMenu.css';

interface DropdownMenuProps {
  isOpen: boolean;
  options: string[];
  selectedOption: string;
  onSelect: (option: string) => void;
  position?: 'left' | 'right';
  className?: string;
}

const DropdownMenu: React.FC<DropdownMenuProps> = ({
  isOpen,
  options,
  selectedOption,
  onSelect,
  position = 'left',
  className = '',
}) => {
  if (!isOpen) return null;

  return (
    <div 
      className={`dropdown-menu ${position} ${className}`}
      role="listbox"
      aria-label="Search categories"
    >
      {options.map((option) => (
        <div 
          key={option} 
          className={`dropdown-item ${selectedOption === option ? 'selected' : ''}`}
          onClick={() => onSelect(option)}
          role="option"
          aria-selected={selectedOption === option}
        >
          {option}
        </div>
      ))}
    </div>
  );
};

export default DropdownMenu;