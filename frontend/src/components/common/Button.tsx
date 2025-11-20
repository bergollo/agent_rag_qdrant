import React from 'react';


interface ComponentProps {
  className?: string;
  children?: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

const Button: React.FC<ComponentProps> = ({ className, children, onClick, disabled }) => {

    return (
        <button 
        className={`bg-gray-400 border border-transparent rounded-md px-4 py-2 text-base font-medium text-black hover:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${className}`}
        onClick={onClick}
        disabled={disabled}
        >
            {children}
        </button>
    );
}

export default Button;