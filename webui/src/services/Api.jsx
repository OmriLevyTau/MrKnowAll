import axios from "axios";

const serverURL = window.location.origin.replace("3000","8000")
const DOCUMENTS_URL = serverURL + "/api/v0/documents"
const CHAT_URL = serverURL + "/api/v0/query"

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
        console.log(result)
        return result
    } catch(e){
        return e
    }
}

export const deleteDocument = async (doc_id) => {
    let config = {
        method: 'delete',
        maxBodyLength: Infinity,
        url: DOCUMENTS_URL + "/" + doc_id,
        headers: { }
    };
    try{
        const result = await axios.request(config)
        console.log(result)
        return result
    } catch(e){
        return e
    }
}

export const query = async (query) => {
    let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: CHAT_URL,
        headers: { 
          'Content-Type': 'application/json'
        },
        data : query
      };

    try{
        const result = await axios.request(config)
        console.log(result)
        return result
    } catch(e){
        return e
    }

}