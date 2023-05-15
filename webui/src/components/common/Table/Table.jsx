import { Table, Button, Modal, Upload, name } from "antd";
import { useContext, useState } from "react";
import { DeleteOutlined, FileTextOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { ChatLogContext } from "../../pages/AppContent/ChatContext";

function FileTable() {
  const navigate = useNavigate();
  const [file, setFile] = useState();
  const {dataSource, setDataSource} = useContext(ChatLogContext);


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
        setDataSource((pre) => {
          return pre.filter((file) => file.name !== record.name);
        });
      },
    });
  };

  const UploadFile = (event) => {
    const uploadedFile = event.file;
    const newFile = {
      name: uploadedFile.name.split(".")[0],
      size: `${Math.round(uploadedFile.size / 1024)} KB`,
      dateModified: new Date().toLocaleDateString(),
    };
    const isFileExists = dataSource.some((file) => file.name === newFile.name);
    if (!isFileExists) {
      setDataSource((pre) => [...pre, newFile]);
    }
  };

  return (
    <div style={{display: "flex", flexDirection:"column", width:"97%", alignItems:"center"}} >
        <Upload name="File" onChange={UploadFile} fileList={null} >
          <Button type="primary">
            Upload File
          </Button>
        </Upload>
        <Table columns={columns} dataSource={dataSource} style={{paddingTop:"3%", width:"100%"}} rowKey="name" ></Table>
    </div>
  );
}

export default FileTable;
