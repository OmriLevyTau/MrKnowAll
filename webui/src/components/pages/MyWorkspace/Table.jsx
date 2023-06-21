import { Table, Modal, Spin, Result,  } from "antd";
import { useContext, useEffect, useState,} from "react";
import { DeleteOutlined, FileTextOutlined, LoadingOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../../pages/AppContent/AppContext";
import { uploadDocument, deleteDocument, getAllDocsMetaData } from "../../../services/Api";
import DragFile from "./DragFile";
import useFileStore from "./store";
import GenericModal from "../../common/Modal/GenericModal"
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { CheckOutlined } from "@mui/icons-material";


function FileTable() {
  const navigate = useNavigate();
  const [prefetched, setPrefetched] = useState(false)
  const [pdfFile, setPdfFile] = useState(null);
  const [fileMetaData, setFileMetaData] = useState(null);

  const { user, token } = useContext(UserContext);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const { files, addFileToStore, removeFileFromStore,updateFileInStore, setAllFiles } = useFileStore();

  /**
   * {
   *  file1: {metadata: null, pdfFile: null, loading: false },
   *  file2: {metadata: null, pdfFile: null, loading: false }
   * }
   */

  const queryClient = useQueryClient()

  const {data} = useQuery({
      queryKey:["docs"], 
      queryFn: () => getInitialData(user.email), 
      enabled: user!=null,
      refetchOnWindowFocus: false
    },
  )

  // Fetch initial data
  // ======================================================

  const getInitialData = async (user_id) => {
    let initialDataResponse = await getAllDocsMetaData(user_id, token);
    if (initialDataResponse.status!==200 && initialDataResponse.status!==204){
      alert("An error occured while trying to fetch initial data.");
      return []
    }
    let docs = initialDataResponse.data ? initialDataResponse.data.docs_metadata : null
    if (docs == null){return [];}
    
    docs = docs.map((d) => ({
      name: d.document_id,
      size: `${Math.round(d.document_size / 1024)} KB`,
      dateModified: d.creation_time,
    }))
    return docs;
  }

  const prefetch = async () => {
    // if (!prefetched){
      await queryClient.prefetchQuery({queryKey:['docs'], queryFn: () => getInitialData(user.email)});
      setPrefetched(true);
    // }
  }


  useEffect(()=>{
    // solves problem of zustand store get cleared
    // on refresh when standing on "my-workspace".
    if (data && data.length > 0){
      setAllFiles(data)
    }
  },[data])
  

  // Helpers and configs
  // ======================================================
  const onCancel = () => {
    if (!loading){
      setOpen(false);
      setLoading(false);
      setPdfFile(null);
      setFileMetaData(null);
    }    
  }

  const columns = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
      sorter: (record1, record2) => {
        return record1.name.localeCompare(record2.name);
      },
    },
    {
      title: "Size",
      dataIndex: "size",
      key: "size",
    },
    {
      title: "Date Modified",
      dataIndex: "dateModified",
      key: "dateModified",
    },
    {
      title: "Progress",
      key: "progress",
      render: (record) => {
        return (
          <>
            {loading ? <Spin indicator={<LoadingOutlined style={{fontSize:24}} />} /> : <CheckOutlined /> }
          </>
        )
      }
    },
    {
      title: "Action",
      key: "action",
      render: (record) => {
        return (
          <>
            <DeleteOutlined onClick={() => onDeleteFile(record)} />
            <FileTextOutlined
              style={{ color: "black", marginLeft: 10 }}
              onClick={() => navigate("/doc-view/" + record.name)}
            />
          </>
        );
      },
    },
  ];

  // Delete a File
  // ======================================================
  const onDeleteFile = (record) => {
    Modal.confirm({
      title: "Are you sure you want to delete this file?",
      okText: "yes",
      cancelText: "No",
      okType: "danger",
      onOk: () => {
        deleteDocument(user.email, record.name, token); // backend
        removeFileFromStore(record.name);
      },
    });
  };

  // Upload a File
  // ======================================================

  const onUploadFile = async () => {
    setLoading(true);
    try {
      const newFile = {
        name: fileMetaData.name.split(".")[0],
        size: `${Math.round(fileMetaData.size / 1024)} KB`,
        dateModified: new Date().toLocaleDateString(),
      };
  
      let filePayload = {
        "document_metadata": {
            "user_id": user.email,
            "document_id": newFile.name,
        },
        "pdf_encoding": pdfFile
      }

      let uploadDocResponse = await uploadDocument(filePayload, token); // backend
    

    // check if error occured when communicating with the backend
    if (uploadDocResponse.status!==200 && uploadDocResponse.status!==204){
      alert("An error occured while trying uploading the file. Please try again.");
      return; // finally will exectue of course.
    }

    // Otherwise, it was successfull. Add the file to the table.
    addFileToStore(newFile);

    }
    finally{
      setOpen(false);
      setPdfFile(null);
      setFileMetaData(null);
      setLoading(false);
    }
  }

  // Async upload a File
  // ======================================================

  const onAsyncUploadFile = async () => {
    setLoading(true);
    try {
      const newFile = {
        name: fileMetaData.name.split(".")[0],
        size: `${Math.round(fileMetaData.size / 1024)} KB`,
        dateModified: new Date().toLocaleDateString(),
      };
  
      let filePayload = {
        "document_metadata": {
            "user_id": user.email,
            "document_id": newFile.name
        },
        "pdf_encoding": pdfFile
      }
    addFileToStore(newFile);

    uploadDocument(filePayload)
      .then((uploadDocResponse) => {
        // check if error occured when communicating with the backend
        if (uploadDocResponse.status!==200 && uploadDocResponse.status!==204){
          alert("An error occured while trying uploading the file. Please try again.");
          return; // finally will exectue of course.
        }
        // Otherwise, it was successfull. Add the file to the table.
        setLoading(false);
      })
    }
    finally{
      setOpen(false);
      setPdfFile(null);
      setFileMetaData(null);
    }
  }


  const content = 
    <div>
      <DragFile 
        onCancel={onCancel}
        onSubmit={onAsyncUploadFile}
        setFile={setPdfFile}
        setFileMetaData={setFileMetaData}
        loading={loading}
      />
    </div>

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: "97%",
        alignItems: "center",
      }}
    >
      <GenericModal
            open={open} 
            setOpen={setOpen}
            loading={loading}
            setLoading={setLoading} 
            onCancel={null}
            modalButtonText="upload"
            modalTitle={"Upload File"}
            modalContent={content}            
      />
      <Table
        columns={columns}
        dataSource={files}
        style={{ paddingTop: "3%", width: "100%" }}
        rowKey="name"
      ></Table>
    </div>
  );
}

export default FileTable;