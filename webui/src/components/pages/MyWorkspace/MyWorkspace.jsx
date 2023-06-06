import { useContext } from "react";
import SideMenu from "../../common/Menu/SideMenu";
import FileTable from "./Table";
import { UserContext } from "../AppContent/AppContext";
import ChatInput from "../Chat/ChatInput";

function MyWorkspace() {
  const { user } = useContext(UserContext);

  return (
    <>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          background: "white",
          height: "100%",
          width: "flex-grow",
        }}
      >
        <SideMenu />
        <div
          style={{
            flexGrow: 1,
            width: "100%",
            height: "100%",
            borderLeft: "15px white solid",
            overflowY: "visible",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
          }}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              position: "relative",
            }}
          >
            <div
              style={{
                alignItems: "center",
                fontFamily: "Nunito, sans-serif",
                fontSize: "180%",
              }}
            >
              {/* <h1>{user && user.email.split("@")[0]}-workspace</h1> */}
              <h1
                style={{
                  textAlign: "center",
                  fontFamily: "Nunito, sans-serif",
                  width: "97%",
                  fontSize: "200%",
                  fontWeight: 800,
                  marginBottom: "1%",
                }}
              >
                my workspace
              </h1>
            </div>
          
            <div style={{display:"flex", position:"relative", marginTop:"1.5%"}}>
              <FileTable></FileTable>
            </div>
          </div>
          <div>
            <div
              className="new-home-header-search"
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                position: "relative",
              }}
            >
              <h3
                style={{
                  color: "black",
                  fontWeight: "700",
                  fontFamily: "Nunito, sans-serif",
                }}
              ></h3>
              <ChatInput width={"80%"} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default MyWorkspace;
