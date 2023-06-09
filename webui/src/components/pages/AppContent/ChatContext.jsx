import { createContext, useState } from "react";

export const ChatLogContext = createContext();

/**
 * 
 * @deprecated
 * We're using {@link chatStore.js} instead.
 */
function ChatContext(props) {
  const [chatLog, setChatLog] = useState([]);
  const [dataSource, setDataSource] = useState([]);

  // get user data from backend for initial display.

  return (
    <ChatLogContext.Provider
      value={{ chatLog, setChatLog, dataSource, setDataSource }}
    >
      {props.children}
    </ChatLogContext.Provider>
  );
}

export default ChatContext;
