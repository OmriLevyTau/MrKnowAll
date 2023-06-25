import { useNavigate, useParams } from "react-router-dom";
import { Button } from "antd";
import { useContext, useEffect, useState } from "react";
import { UserContext } from "../AppContent/AppContext";
import { getDocById } from "../../../services/Api";
import { ArrowBack } from "@mui/icons-material";

function DocView() {
  const { fileName } = useParams();
  const navigate = useNavigate();
  const [fileContent, setFileContent] = useState(null);
  const { user , token} = useContext(UserContext);

  useEffect(() => {
    async function fetchFile() {
      try {
        const response = await getDocById(user.email, fileName, token)
        // Create a Blob URL for the file content
        const blobUrl = URL.createObjectURL(response.data);
        setFileContent(blobUrl);
      } catch (error) {
        alert("File does not exist! " + error.message);
      }
    }

    fetchFile();
  }, [fileName]);

  return (
    <div className="doc-view" style={{ overflow: "hidden" }}>
      <div
        className="doc-actions"
        style={{
          display: "flex",
          flexDirection: "row",
          backgroundColor: "rgb(50,50,50)",
          height: "7vh",
        }}
      >
        <div style={{ position: "absolute", left: "40%", paddingTop: "1%" }}>
          <font size="+1" style={{ color: "white" }}>
            {fileName}
          </font>
        </div>
        <Button
          color="rgb(50,50,50)"
          onClick={() => navigate(-1)}
          style={{ left: "87%", top: "20%" }}
        >
          <ArrowBack style={{ fontSize:"20px" }} />
          {/* <img src={backArrow} style={{ height: "100%", width: "100%" }} /> */}
        </Button>
      </div>
      <object
        data={
          fileContent
            ? `${fileContent}#zoom=140&scrollbar=0&toolbar=0&navpanes=0`
            : null
        }
        style={{ width: "100vw", height: "100vh" }}
      />
    </div>
  );
}

export default DocView;
