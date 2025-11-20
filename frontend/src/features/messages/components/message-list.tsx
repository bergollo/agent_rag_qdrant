// message-list.tsx
import React, { useEffect, useRef } from 'react';
import { useAppSelector } from "../../../app/hooks";
// import { selectMessagesForConversation, selectMessagesLoading, selectAllMessages } from '../messagesSelectors';
import { selectMessagesLoading, selectAllMessages } from '../messagesSelectors';
import MessageBubble from '../../../components/common/MessageBubble';

interface ComponentProps {
  className?: string;
}

const MessageList: React.FC<ComponentProps> = ({ className }) => {
  // const messages = useAppSelector(selectMessagesForConversation(conversationId));
  const messages = useAppSelector(selectAllMessages);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const loading = useAppSelector(selectMessagesLoading);
  const bottomRef = useRef<HTMLDivElement | null>(null);

//   TODO: Remove Code - Belongs in MessageInput Component
//   const handleSendMessage = () => {
//     if (newMessage.trim()) {
//       setMessages([...messages, { id: Date.now(), text: newMessage, sender: 'user' }]);
//       setNewMessage('');
//     }
//   };

  useEffect(() => {
    containerRef.current?.scrollTo({ top: containerRef.current.scrollHeight, behavior: "smooth" });
  }, [messages.length]);

  return (
    <div className={`mb-2 ${className}`}>
        <div className="flex flex-col w-full min-h-80 max-h-[400px] bg-gray-100 dark:bg-gray-500 rounded-lg shadow-lg border border-gray-300">
            <>
            {(loading && messages.length === 0) ? 
                (<div style={styles.info}>Loading messages…</div>)

            : (!loading && messages.length === 0) ?
                (<div style={styles.info}>No messages yet. Say hi! 👋</div>)
            : (
                <div ref={containerRef} className="flex-grow p-4 overflow-y-auto">
                  {messages.map((message) => (
                  <MessageBubble
                      key={message.id}
                      message={message}
                      isOwn={ message.sender === 'user' }
                  />
                  ))}
                  <div ref={bottomRef} />
                </div>
              )}
            </>
        </div>
    </div>
  );
};

export default MessageList;

// ------------------------
// Inline styles for demo
// Replace with your CSS
// ------------------------
const styles: { [key: string]: React.CSSProperties } = {
  container: {
    flex: 1,
    overflowY: "auto",
    padding: "12px",
    backgroundColor: "#f5f5f5",
    display: "flex",
    flexDirection: "column",
  },
  info: {
    padding: "16px",
    textAlign: "center",
    color: "#777",
  },
  messageRow: {
    display: "flex",
    marginBottom: "8px",
  },
  bubble: {
    maxWidth: "70%",
    padding: "8px 10px",
    borderRadius: "12px",
    boxShadow: "0 1px 1px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column",
  },
  text: {
    fontSize: "0.95rem",
    marginBottom: "4px",
    wordBreak: "break-word",
  },
  meta: {
    fontSize: "0.75rem",
    color: "#777",
    textAlign: "right",
  },
};