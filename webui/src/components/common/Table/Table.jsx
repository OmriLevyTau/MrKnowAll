import { Table, Button, Modal, Upload, name } from "antd";
import { useContext, useState } from "react";
import { DeleteOutlined, FileTextOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { ChatLogContext } from "../../pages/AppContent/ChatContext";
import { UserContext } from "../../pages/AppContent/AppContext";
import axios from "axios";
import Dragger from "antd/es/upload/Dragger";

function FileTable() {
  const navigate = useNavigate();
  const [pdfFile, setPdfFile] = useState();
  const { dataSource, setDataSource } = useContext(ChatLogContext);
  const { user } = useContext(UserContext);

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
    if (event.file.status !== "uploading") {
      console.log("Here!");
      let reader = new FileReader();
      reader.onload = (e) => {
        console.log(e.target.result);
        setPdfFile(e.target.result);
        console.log("FILEEEEE");
      };
      reader.readAsDataURL(event.file.originFileObj);
    } else {
      console.log("Error");
    }
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
  /*
  const UploadFile = async (event) => {
    const uploadedFile = event.file;
    const formData = new FormData();
    formData.append("file", uploadedFile);
    formData.append("user_name", user);
    console.log(formData);

    try {
      const newFile = {
        name: uploadedFile.name.split(".")[0],
        size: `${Math.round(uploadedFile.size / 1024)} KB`,
        dateModified: new Date().toLocaleDateString(),
      };
      const isFileExists = dataSource.some(
        (file) => file.name === newFile.name
      );
      if (!isFileExists) {
        setDataSource((prev) => [...prev, newFile]);
      }
      const response = await axios.post(
        "http://localhost:8000/gooogle/upload",
        formData
      );

      if (response.status === 200) {
        console.log("File uploaded successfully");
      } else {
        console.error("Upload fail");
      }
    } catch (error) {
      console.error("An error occurred during upload", error);
    }
  };
  */

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: "97%",
        alignItems: "center",
      }}
    >
      <Dragger name="File" onChange={UploadFile}>
        <Button type="primary">Upload File</Button>
      </Dragger>
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
