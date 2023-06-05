import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import { mountStoreDevtool } from 'simple-zustand-devtools';

/**
 * A quick note on storage:
 * localStorage: 
 *  provides a way to store key-value pairs in the browser that persist even 
 *  after the browser is closed and reopened.
 * sessionStorage:
 *  similar to localstorage but is only available for the 
 *  duration of the current browser session.
 */

const useFileStore = create(
    persist(
        (set) => ({
            files: [],
            // Method to add a file to the list
            addFileToStore: (file) => {set((state) => ({files: [...state.files, file]}));},
            removeFileFromStore: (name) => {set((state) => ({files: state.files.filter((file) => file.name !== name)}));},
      }), 
      {
        name: 'files-storage', // name of the item in the storage (must be unique)
        storage: createJSONStorage(() => sessionStorage), // (optional) by default, 'localStorage' is used
      } 
    )
);

  mountStoreDevtool("File Store", useFileStore);
  export default useFileStore;