import React from "react";
import type { Message } from "../../types/messages";

// ------------------------
// Message bubble component
// ------------------------
interface ComponentProps {
  message: Message;
  isOwn: boolean;
  key: React.Key;
}

const MessageBubble: React.FC<ComponentProps> = ({ message, isOwn, key }) => {
  const { text, createdAt } = message;

  const formattedTime = new Date(createdAt).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div
      key={key}
      className={`message-bubble flex mb-2 ${isOwn ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`
          min-w-30 max-w-3/4 px-2 py-4 rounded-lg shadow-sm flex flex-col 
          ${isOwn ? "justify-end bg-blue-300" : "justify-start bg-green-300"}
          `}
      >
        <div className="font-medium mb-1 break-words">{text}</div>
        <div className="text-xs text-gray-600 text-right">{formattedTime}</div>
      </div>
    </div>
  );
};

export default MessageBubble;