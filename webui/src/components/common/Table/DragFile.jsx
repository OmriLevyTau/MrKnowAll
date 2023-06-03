import { Button, Space, Spin } from "antd";
import { InboxOutlined } from "@mui/icons-material";
import Dragger from "antd/es/upload/Dragger";


function DragFile(props) {

    const {onCancel, onSubmit, setFile, setFileMetaData, dataSource, setDataSource, loading} = props;

    const onChange = (event) => {
        if (event.file.status !== "uploading") {
          let reader = new FileReader();
          reader.onload = (e) => {
            setFile(e.target.result);
            setFileMetaData(event.file)
          };
          reader.readAsDataURL(event.file.originFileObj);
        } else {
          console.log("Error");
        }
      };
    

    return (
        <div className="drag-file">
        <Space direction="vertical">
            <p>currently, only pdf files are accepted.</p>
            {loading ? <Spin top="Loading" size="large" /> :
             <Dragger name="File" onChange={onChange} accept=".pdf">
                <p><InboxOutlined /></p>
                <p>Click here or drag</p>
            </Dragger>}
            <div>
            <Space>
                <Button key="cancel" onClick={onCancel} disabled={loading} >Cancel</Button>
                <Button key="submit" type="primary" onClick={onSubmit} disabled={loading} >Upload</Button>
            </Space>
            </div>
        </Space>
        </div>
    )
}

export default DragFile