// chat-header.tsx
import React from 'react';

interface ComponentProps {
  className?: string;
}

const ChatHeader: React.FC<ComponentProps> = ({ className }) => {
  return (
    <div className={`chat-header ${className}`}>
      <h2>Experimental Chatbot</h2>
    </div>
  );
};

export default ChatHeader;