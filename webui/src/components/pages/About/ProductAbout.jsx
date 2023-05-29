
import React from 'react'
import workflowUpload from "../../../images/workflow-upload.png"
import workflowAsk from "../../../images/workflow-ask.png"


function ProductAbout({title, description, imageName, reverse}) {
  

    if (!reverse){
      return(
        <div className="landing-product" style={{ display:"flex", flexDirection:"row", marginTop:"7%" }}>
          <div className="product-description" style={{display:"flex", flexDirection:"column", justifyContent:"flex-start", marginRight:"0%" }} >
            <h3 style={{fontSize: `max(20px, 1.8vw)`}} >{title}</h3>
            <p style={{fontSize: `max(16px, 1.2vw)`}} >{description}</p>
          </div>
          <div className="product-imgae"  style={{display:"flex", justifyContent:"end"}} >
            <img src={ workflowUpload } alt="workflow"  style={{ height:"90%", width:"90%", aspectRatio:"auto" }} />
          </div>        
        </div>
      )
    }
  return (
      <div className="landing-product" style={{ display:"flex", flexDirection:"row", marginTop:"10%" }}>
        <div className="product-imgae"  style={{display:"flex", justifyContent:"start", marginRight:"3%",}} >
          <img src={ workflowAsk}  alt="workflow" style={{ height:"95%", width:"95%", aspectRatio:"auto" }} />
        </div>
        <div className="product-description" style={{display:"flex", flexDirection:"column", justifyContent:"flex-start" }} >
          <h3 style={{fontSize: `max(20px, 1.8vw)`}} >{title}</h3>
          <p style={{fontSize: `max(16px, 1.2vw)`}} >{description}</p>
        </div>       
    </div>
  )
}

export default ProductAbout