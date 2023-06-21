import axios from "axios";

const serverURL = window.location.origin.replace("3000","8000")
const DOCUMENTS_URL = serverURL + "/api/v0/documents"
const CHAT_URL = serverURL + "/api/v0/query"


export const uploadDocument = async (data, token) => {
    console.log("called uploadDocument");
    let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: DOCUMENTS_URL,
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        data : data,
    };
    try{
        const result = await axios.request(config)
        return result
    } catch(e){
        return e
    }
}

export const deleteDocument = async (user_id, doc_id, token) => {
    console.log("called deleteDocument");
    let config = {
        method: 'delete',
        maxBodyLength: Infinity,
        url: DOCUMENTS_URL + "/" + doc_id,
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        data: {user_id: user_id}
        
    };
    try{
        const result = await axios.request(config)
        return result
    } catch(e){
        return e
    }
}

export const query = async (query, token) => {
    console.log("called query");
    let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: CHAT_URL,
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        data : query
      };

    try{
        const result = await axios.request(config)
        return result
    } catch(e){
        return e
    }
}


export const getDocById = async (user_id, doc_id, token) => {
    console.log("called getDocById");
    let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: DOCUMENTS_URL + "/" + user_id + "/" + doc_id,
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        responseType: "blob"
      };

    try{
        const result = await axios.request(config)
        return result
    } catch(e){
        return e
    }
}

export const getAllDocsMetaData = async (user_id, token) => {
    console.log("called getAllDocsMetaData");
    let config = {
        method: 'get',
        url: DOCUMENTS_URL + "/" + user_id,
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
      };

    try{
        const result = await axios.request(config)
        return result
    } catch(e){
        return e
    }
}