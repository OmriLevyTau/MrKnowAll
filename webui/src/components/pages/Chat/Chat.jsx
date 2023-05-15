import  { useContext, useEffect, useRef } from 'react';
import ChatInput from './ChatInput';
import ChatLog from './ChatLog';
import SideMenu from '../../common/Menu/SideMenu';
import { ChatLogContext } from '../AppContent/ChatContext';


function Chat(){
    const messageRef = useRef();
    const { chatLog } = useContext(ChatLogContext);

    useEffect(() => {
      if (messageRef.current) {
        messageRef.current.scrollIntoView(
          {
            behavior: 'smooth',
            block: 'end',
            inline: 'nearest'
          })
      }
    },
    [chatLog])


  return (
    <div
      className="chat"
      style={{
        display: "flex",
        flexDirection: "row",
        background: "white",
        height: "100%",
        width: "100%",
      }}
    >
      <SideMenu />
      <div
        className="chat-content"
        style={{
          display: "flex",
          flexDirection: "column",
          width: "100%",
          height: "100%",
          alignItems: "center",
          borderLeft: "1px grey solid",
          overflowY: "scroll",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            height: "100%",
            width: "80%",
            justifyContent: "space-between",
            paddingBottom: "1.5%",
          }}
        >
          <ChatLog />
          <div ref={messageRef}>
            <ChatInput width={"100%"} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
