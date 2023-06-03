import axios from "axios";

const serverURL = window.location.origin.replace("3000","8000")
const DOCUMENTS_URL = serverURL + "/api/v0/documents"
const CHAT_URL = serverURL + "/api/v0"

export const uploadDocument = async (data) => {
    let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: DOCUMENTS_URL,
        headers: { 
          'Content-Type': 'application/json'
        },
        data : data
    };
    try{
        const result = await axios.request(config)
    } catch(e){
        return e
    }
}

export const deleteDocument = async (doc_id) => {
    console.log(doc_id);
    let config = {
        method: 'delete',
        maxBodyLength: Infinity,
        url: DOCUMENTS_URL + "/" + doc_id,
        headers: { }
    };
    try{
        const result = await axios.request(config)
    } catch(e){
        return e
    }

}