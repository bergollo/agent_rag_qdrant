// chat-container.tsx
import React from 'react';
import ChatHeader from './chat-header';
import MessageList from './message-list';
import MessageInput from './message-input';

interface ComponentProps {
  className?: string;
}

const ChatContainer: React.FC<ComponentProps> = ({ className }) => {
  return (
    <div className={`chat-container ${className}`}>
      <ChatHeader />
      <MessageList />
      <MessageInput /> 
    </div>
  );
};

export default ChatContainer;