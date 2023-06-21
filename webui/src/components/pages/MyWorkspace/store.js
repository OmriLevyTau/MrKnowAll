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
 * 
 * files: 
 * [
 *  file1: {name: file1, size: null, dateModified: null, pdfFile: null, loading: false },
 *  file2: {name: file2, size: null, dateModified: null, pdfFile: null, loading: false }
 * ]
 * 
 */

const useFileTableStore = create(
    persist(
        (set) => ({
            files: [],
            addFileToStore: (file) => {set((state) => ({files: [...state.files, file]}));},
            removeFileFromStore: (name) => {set((state) => ({files: state.files.filter((file) => file.name !== name)}));},
            updateFileInStore: (file) => {
                set((state) => ({
                  files: state.files.map(
                    (f) => (f.name === file.name ? [...state.files, file] : [...state.files, f])
                    )
                }))
              },
            setAllFiles: (docs) => {set((state) => ({files: [...docs]}) )}
      }), 
      {
        name: 'files-storage', // name of the item in the storage (must be unique)
        storage: createJSONStorage(() => sessionStorage), // (optional) by default, 'localStorage' is used
      } 
    )
);

mountStoreDevtool("File Store", useFileTableStore);
export default useFileTableStore;

