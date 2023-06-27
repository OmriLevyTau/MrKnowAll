import ChatMessage from "./ChatMessage";
import useChatStore from "./chatStore";

/**
 *
 * Message in log:
 *  {
 *      chatgpt: boolean
 *      content: String
 *  }
 */
function ChatLog() {
  const {chatMsg} = useChatStore();
  const msgArray = chatMsg.map((msg, index) => (
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
