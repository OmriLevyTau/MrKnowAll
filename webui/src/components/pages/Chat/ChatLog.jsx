import { useContext } from "react";
import { UserContext } from "../AppContent/AppContext";
import { ChatLogContext } from "../AppContent/ChatContext";
import ChatMessage from "./ChatMessage";

/**
 *
 * Message in log:
 *  {
 *      chatgpt: boolean
 *      content: String
 *  }
 */
function ChatLog() {
  const { chatLog } = useContext(ChatLogContext);
  const msgArray = chatLog.map((msg, index) => (
    <ChatMessage chatgpt={msg.chatgpt} content={msg.content} key={index} />
  ));

  return (
    <div
      className="chat-log"
      style={{
        marginBottom: "3%",
        marginTop: "3%",
        textAlign: "left",
        width: "100%",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {msgArray}
    </div>
  );
}

export default ChatLog;
