import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import { mountStoreDevtool } from 'simple-zustand-devtools';


const useChatStore = create(
    persist(
        (set) => ({
            chatMsg: [],
            addMsgToStore:  (msg) => {set((state) => ({chatMsg: [...state.chatMsg, msg]}));},
            removeLastMsgFromStore: (msg) => {set((state) => ({chatMsg: [...state.chatMsg.slice(0,-1)]}));},
            clearChatStore: () => {set((state) => ({chatMsg: []}) )}
      }), 
      {
        name: 'chat-storage', // name of the item in the storage (must be unique)
        storage: createJSONStorage(() => sessionStorage), // (optional) by default, 'localStorage' is used
      } 
    )
);

mountStoreDevtool("Chat Store", useChatStore);
export default useChatStore;

