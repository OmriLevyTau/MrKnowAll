import { Button, Space, Spin } from "antd";
import { InboxOutlined } from "@mui/icons-material";
import Dragger from "antd/es/upload/Dragger";

/**
 * 
 * files: 
 * [
 *  file1: {name: file1, size: null, dateModified: null, loading: false },
 *  file2: {name: file2, size: null, dateModified: null, loading: false }
 * ]
 */
function DragFile(props) {

    const {onCancel, onRemove, onSubmit, setFile, setFileMetaData, loading} = props;
    const dateModified = new Date().toLocaleDateString()

    const onChange = (event) => {
        if (event.file.status !== "uploading") {
          let reader = new FileReader();
          reader.onload = (e) => {
            setFile(e.target.result);
            setFileMetaData(event.file);
          };
          reader.readAsDataURL(event.file.originFileObj);
        }
      };
    

    return (
    <div className="drag-file" style={{ display: "flex", flexDirection: "column" }}>
      <Space direction="vertical" style={{ width: "100%" }}>
        <p>Note: currently, only pdf files are accepted.</p>
        <div className="dragger-holder" >
          {loading ? (
            <Spin top="Loading" size="large" style={{ width: "100%", display: "flex", justifyContent:"center" }} />
          ) : (
            <Dragger name="File" onChange={onChange} onRemove={onRemove} on accept=".pdf" style={{ width: "100%", display: "flex" }} >
              <p><InboxOutlined /></p>
              <p>Click here or drag.</p>
            </Dragger>
          )}
        </div>
        <div className="dragger-buttons" style={{ width: "100%", display: "flex", justifyContent: "flex-end" }}>
          <Space>
            {/* <Button key="cancel" onClick={onCancel} disabled={loading}>Cancel</Button> */}
            <Button key="submit" type="primary" onClick={onSubmit} disabled={loading}>Upload</Button>
          </Space>
        </div>
      </Space>
    </div>

    )
}

export default DragFile