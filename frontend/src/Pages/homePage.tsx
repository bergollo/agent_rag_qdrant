import React from "react";
import HealthCheckButton from "../features/connectionCheck/components/connectionCheck";
import ChatContainer from "../features/messages/components/chat-container";

const HomePage: React.FC = () => {
  return (
    <div className="min-w-[800px] p-8  rounded-lg shadow-lg">
      <h1>MCP React UI</h1>
      <HealthCheckButton className="float-right"/>
      <ChatContainer />
    </div>
  );
}
export default HomePage;