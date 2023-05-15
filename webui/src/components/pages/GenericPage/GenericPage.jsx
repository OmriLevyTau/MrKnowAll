import TopMenu from "../../common/Menu/TopMenu";

function GenericPage(props){
    const {title, description, page} = props;

    return(
        <div className="generic-layout">
            <div className="generic-header">
                <div className="generic-header-title"><h1>{title}</h1></div>
                <div className="generic-header-description">{description}</div>
            </div>
            <div className="generic-page-content">
                {page}
            </div>
        </div>
    )
}

export default GenericPage;