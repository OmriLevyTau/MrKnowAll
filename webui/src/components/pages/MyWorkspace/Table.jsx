import { Table, Modal,  } from "antd";
import { useContext, useState,} from "react";
import { DeleteOutlined, FileTextOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../../pages/AppContent/AppContext";
import { uploadDocument, deleteDocument } from "../../../services/Api";
import DragFile from "./DragFile";
import useFileStore from "./store";
import GenericModal from "../../common/Modal/GenericModal"

function FileTable() {
  const navigate = useNavigate();
  const [pdfFile, setPdfFile] = useState(null);
  const [fileMetaData, setFileMetaData] = useState(null);

  const { user } = useContext(UserContext);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const { files, addFileToStore, removeFileFromStore } = useFileStore();


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
        deleteDocument(user.email, record.name); // backend
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
            "document_id": newFile.name
        },
        "pdf_encoding": pdfFile
      }

      let uploadDocResponse = await uploadDocument(filePayload); // backend

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


  const content = 
    <div>
      <DragFile 
        onCancel={onCancel}
        onSubmit={onUploadFile}
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