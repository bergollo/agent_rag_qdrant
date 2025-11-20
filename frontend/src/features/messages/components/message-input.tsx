// message-input.tsx
import React, { useState, type KeyboardEvent } from 'react';
import { SquareX } from 'lucide-react'

import type { Message } from "../../../types/messages";
import { useAppDispatch, useAppSelector } from "../../../app/hooks";
import { addMessage, deleteMessage, messageQuery } from "../messagesSlice";
import { selectMessagesLoading, selectAllMessages } from "../messagesSelectors";
import { selectStoreDocumentLoading } from '../../storeDocument/storeDocumentSelector';
import { v4 as uuid } from "uuid";
import Button from '../../../components/common/Button';
import UploadButton from '../../storeDocument/components/upload-button';


interface ComponentProps {
  className?: string;
}

const MessageInput: React.FC<ComponentProps> = ({ className }) => {
  const dispatch = useAppDispatch();
  const messages = useAppSelector(selectAllMessages);
  const loading = useAppSelector(selectMessagesLoading);
  const storeDocLoading = useAppSelector(selectStoreDocumentLoading);

  const [text, setText] = useState('');

  const  sendMessage = async () => {
    if (text.trim()) {
        const tempMsg: Message = { 
          id: uuid(), 
          text, 
          sender: "user", 
          createdAt: new Date().toISOString(), 
          status: "sending" 
        };

        // const res = await fetch("/api/ai/query", {
        // method: "POST",
        // headers: { "Content-Type": "application/json" },
        // body: JSON.stringify({ message: text }),
        // });
        // const data = await res.json();

        dispatch(addMessage(tempMsg)); // optimistic — replace with real send
        await dispatch(messageQuery({ userMessage: tempMsg }));
        setText("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleDeleteMessage = async () => {
    messages.forEach((message) => {
      dispatch(deleteMessage(message.id));
    });
  }

  return (
    <div className={`message-input ${className}`}>
      <div className="flex flex-row w-full min-w-50vh justify-center items-center p-1">
        <SquareX className="mr-2 cursor-pointer hover:text-red-500" size={25} onClick={handleDeleteMessage}/>
        <UploadButton></UploadButton>
        <input
          type="text"
          placeholder="Type a question"
          value={text}
          onKeyDown={handleKeyDown}
          onChange={(e) => setText(e.target.value)}
          className='w-full p-2 rounded-lg shadow-lg border border-gray-300 bg-gray-500'
          disabled={storeDocLoading}
        />
        <Button 
          onClick={sendMessage}
          className="ml-2 shadow-lg"
          disabled={loading || !text}
        >
          Send
        </Button>
      </div>
    </div>
  );
};

export default MessageInput;
