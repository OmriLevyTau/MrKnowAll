// import { materialCells, materialRenderers } from "@jsonforms/material-renderers";
// import { JsonForms } from "@jsonforms/react";
// import { Button, Space } from "antd";
// import { useState } from "react";

// function Form(props){
    
//     const {loading, setLoading, onSubmit, onCancel,
//             schema, uischema    
//     } = props;
    
//     const [formData, setFormData] = useState(null);

//     return (
//         <div className="container-modal-json-form" style={{width:'100%', display:'flex', flexDirection:'column'}}>
//             <div className="json-form-div" style={{width:'100%', display:'flex', flexDirection:'column', wordWrap:'break-word'}}>
//                 <JsonForms 
//                     schema={schema}
//                     uischema={uischema}
//                     data={formData}
//                     renderers={materialRenderers}
//                     cells={materialCells}
//                     onChange={(state)=>setFormData(state["data"])}
//                     className="JSONFORM"                
//                 />
//             </div>
//             <div className="modal-json-form-buttons">
//                 <Space>
//                     <Button key="cancel" onClick={()=>onCancel()} disabled={loading}>Cancel</Button>
//                     <Button type="primary" key="submit" onClick={()=>onSubmit(formData)} disabled={loading}>Submit</Button>
//                 </Space>

//             </div>

//         </div>

//     );

// }

// export default Form;