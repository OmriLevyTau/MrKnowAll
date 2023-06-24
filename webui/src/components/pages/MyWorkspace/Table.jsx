import { Table, Modal, Spin, Result, Popover,  } from "antd";
import { useContext, useEffect, useState,} from "react";
import { DeleteOutlined, FileTextOutlined, LoadingOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../../pages/AppContent/AppContext";
import { uploadDocument, deleteDocument, getAllDocsMetaData, getInitialData } from "../../../services/Api";
import DragFile from "./DragFile";
import useFileStore from "./fileStore";
import GenericModal from "../../common/Modal/GenericModal"
import { useQuery } from "@tanstack/react-query";
import { CheckOutlined, ErrorOutline } from "@mui/icons-material";

export const LOADING = "loading";
export const DONE = "done";
export const ERROR = "error";

function FileTable() {
  const navigate = useNavigate();
  const [pdfFile, setPdfFile] = useState(null);
  const [fileMetaData, setFileMetaData] = useState(null);

  const { user, token } = useContext(UserContext);
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState(false);
  const { files, addFileToStore, removeFileFromStore, updateFileStatusInStore, setAllFiles } = useFileStore();

  /**
   * [
   *  file1: {name: file1, size: null, dateModified: null,  status: loading/done/error },
   * ]
   */

// Fetch initial data
// ======================================================
  const getUserAllDocsMetaData = async (user_id, token) => {
    if (!user_id || !token){return []};
    let initialDataResponse = await getAllDocsMetaData(user_id, token);
    if (initialDataResponse.status!==200 && initialDataResponse.status!==204){
      return []
    }
    let docs = initialDataResponse.data ? initialDataResponse.data.docs_metadata : null
    if (docs == null){return [];}
    docs = docs.map((d) => ({
      name: d.document_id,
      size: `${Math.round(d.document_size / 1024)} KB`,
      dateModified: new Date(d.creation_time).toLocaleDateString(),
      status: DONE
    }));
    setAllFiles(docs);
  }

  const {data} = useQuery({
      queryKey:["docs"], 
      queryFn: () => getUserAllDocsMetaData(user.email, token), 
      enabled: (token!==undefined && token!=null),
      refetchOnWindowFocus: false,
    },
  )

  // Helpers and configs
  // ======================================================
  const reset = () => {
    setStatus(false);
    setPdfFile(null);
    setFileMetaData(null);
  }

  const onCancel = () => {
    if (status !== LOADING){
      setOpen(false);
      reset();
    }    
  }

  const onRemove = () => {
    console.log("remove.")
    setPdfFile(null);
    setFileMetaData(null);
  }

  const validateFileName = (name) => {
    let pattern = /^[\x00-\x7F]+$/;
    return pattern.test(name);
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
        if (!record.status || record.status === LOADING) {
          return <Spin indicator={<LoadingOutlined style={{ fontSize: 24 }} />} />;
        } else if (record.status === DONE) {
          return <CheckOutlined style={{ color: "green" }} />;
        } else {
          return (
            <Popover content={"Error while proccessing file. Please delete and try again."} trigger="hover">
              <ErrorOutline style={{ color: "red" }}/>
            </Popover>   
          )
        }
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
              onClick={() => onDisplayFile(record)}
            />
          </>
        );
      },
    },
  ];

  // display file
  // ======================================================
  const onDisplayFile = (record) =>{
    if (record.status !== DONE ) { return ; }
    navigate("/doc-view/" + record.name)
  }


  // Delete a File
  // ======================================================
  const onDeleteFile = (record) => {
    if (record.status === LOADING ) { return ; }
    if (record.status === DONE){
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
    } else {
      Modal.confirm({
        title: "Remove record from table",
        okText: "yes",
        cancelText: "No",
        okType: "danger",
        onOk: () => {
          removeFileFromStore(record.name);
        },
      });
    }
  }


  // Upload a File
  // ======================================================

  const onUploadFile = async () => {
    setStatus(true);
    try {
      const newFile = {
        name: fileMetaData.name.split(".")[0],
        size: `${Math.round(fileMetaData.size / 1024)} KB`,
        dateModified: new Date().toLocaleDateString(),
        status: LOADING
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
      updateFileStatusInStore(newFile.name, ERROR);
      return; // finally will exectue of course.
    }

    newFile.status = DONE;
    // Otherwise, it was successfull. Add the file to the table.
    addFileToStore(newFile);

    }
    finally{
      setOpen(false);
      reset();
    }
  }

  // Async upload a File
  // ======================================================
  // file1: {name: file1, size: null, dateModified: null,  status: false }
  const onAsyncUploadFile = async () => {
    if (!fileMetaData || ! pdfFile) {return ; }
    setStatus(true);
    // Make a deep copy so state can be used to upload additional files.
    const pdfFileCopy = JSON.parse(JSON.stringify(pdfFile));
    const fileMetaDataCopy = JSON.parse(JSON.stringify(fileMetaData));
    try {
      const newFile = {
        name: fileMetaDataCopy.name.split(".")[0],
        size: `${Math.round(fileMetaDataCopy.size / 1024)} KB`,
        dateModified: new Date().toLocaleDateString(),
        status: LOADING
      };
  
      let filePayload = {
        "document_metadata": {
            "user_id": user.email,
            "document_id": newFile.name
        },
        "pdf_encoding": pdfFileCopy
      }
      let valid = validateFileName(newFile.name);
      if (!valid){
        alert("Must be english.")
        reset(); 
        return;
      }
      
      addFileToStore(newFile);
      reset();
      uploadDocument(filePayload, token)
        .then((uploadDocResponse) => {
          // check if error occured when communicating with the backend
          if (uploadDocResponse.status!==200 && uploadDocResponse.status!==204){
            updateFileStatusInStore(newFile.name, ERROR);
            return; // finally will exectue of course.
          }
          // update the of this praticular file to done.
          updateFileStatusInStore(newFile.name, DONE);
        })
        .catch( (error) => {
          updateFileStatusInStore(newFile.name, ERROR);
          }
        )
    }
    finally{
      setOpen(false);
    }
  }


  const content = 
    <div>
      <DragFile 
        onCancel={onCancel}
        onRemove={onRemove}
        onSubmit={onAsyncUploadFile}
        setFile={setPdfFile}
        setFileMetaData={setFileMetaData}
        loading={status}
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
            loading={status}
            setStatus={setStatus} 
            onCancel={onCancel}
            modalButtonText="upload"
            modalTitle={"Upload File"}
            modalContent={content}
            buttonType={"primary"}
            buttonSize={"large"}            
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