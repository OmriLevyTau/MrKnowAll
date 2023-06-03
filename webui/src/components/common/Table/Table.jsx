import { Table, Modal,  } from "antd";
import { useContext, useState,} from "react";
import { DeleteOutlined, FileTextOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { ChatLogContext } from "../../pages/AppContent/ChatContext";
import { UserContext } from "../../pages/AppContent/AppContext";
import { uploadDocument, deleteDocument } from "../../../services/Api";
import GenericModal from "../Modal/GenericModal";
import DragFile from "./DragFile";


function FileTable() {
  const navigate = useNavigate();
  const [pdfFile, setPdfFile] = useState(null);
  const [fileMetaData, setFileMetaData] = useState(null);

  const { dataSource, setDataSource } = useContext(ChatLogContext);
  const { user } = useContext(UserContext);
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)


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
            <DeleteOutlined onClick={() => removeFile(record)} />
            <FileTextOutlined
              style={{ color: "black", marginLeft: 10 }}
              onClick={() => navigate("/doc-view/" + record.name)}
            />
          </>
        );
      },
    },
  ];

  const removeFile = (record) => {
    Modal.confirm({
      title: "Are you sure you want to delete this file?",
      okText: "yes",
      cancelText: "No",
      okType: "danger",
      onOk: () => {
        console.log(record)
        deleteDocument(record.name)
        setDataSource((pre) => {
          return pre.filter((file) => file.name !== record.name);
        });
      },
    });
  };


  const onCancel = () => {
    if (!loading){
      setOpen(false);
      setLoading(false);
      setPdfFile(null);
      setFileMetaData(null);
    }
    
  }

  const onUpload = async () => {

    setLoading(true);
    try {
      const newFile = {
        name: fileMetaData.name.split(".")[0],
        size: `${Math.round(fileMetaData.size / 1024)} KB`,
        dateModified: new Date().toLocaleDateString(),
      };
  
      let data = {
        "document_metadata": {
            "user_id": "test",
            "document_id": newFile.name
        },
        "pdf_encoding": pdfFile
      }
      let uploadDocResponse = await uploadDocument(data)
      const isFileExists = dataSource.some((file) => file.name === newFile.name);
      if (!isFileExists) {
        setDataSource((pre) => [...pre, newFile]);
      }
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
        onSubmit={onUpload}
        setFile={setPdfFile}
        setFileMetaData={setFileMetaData}
        dataSource={dataSource}
        setDataSource={setDataSource}
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
        dataSource={dataSource}
        style={{ paddingTop: "3%", width: "100%" }}
        rowKey="name"
      ></Table>
    </div>
  );
}

export default FileTable;