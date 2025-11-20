export type Todo = {
  id: string;
  text: string;
  completed: boolean;
  createdAt: string;
};

export type AuthState = {
  userId?: string;
  token?: string;
  loading: boolean;
};

export type MessageStatus = "sending" | "sent" | "failed" | "received";

export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  createdAt: string;
  status: MessageStatus;
}