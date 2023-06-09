import  { useEffect, useRef, useState } from 'react';
import ChatInput from './ChatInput';
import ChatLog from './ChatLog';
import SideMenu from '../../common/Menu/SideMenu';
import useChatStore from './chatStore';


function Chat(){
  const messageRef = useRef();
  const {chatMsg} = useChatStore();

  useEffect(() => {
    if (messageRef.current) {
      messageRef.current.scrollIntoView(
        {
          behavior: 'smooth',
          block: 'end',
          inline: 'nearest'
        })
    }
  },)



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
            paddingBottom: "1.5%",
            justifyContent:"space-between"
          }}
        >
          <ChatLog />
          <div ref={messageRef}>
            <ChatInput width={"100%"} withAdvancedFiltering={true} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
