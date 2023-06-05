import { Button, Modal } from "antd";


function GenericModal(props){
    
    const {
        open, setOpen,
        loading, setLoading,
        onCancel,
        modalButtonText, modalTitle,
        modalContent
    } = props;

    const showModal = () => {setOpen(true)}
    const handleCancel = () => {onCancel != null ? onCancel() : setOpen(false)}
    
    return(
        <div>
            {
                modalButtonText!=null ? 
                <Button type="primary" onClick={showModal} footer={null} size="large" style={{width:"100%"}}>
                    {modalButtonText}
                </Button> : null
            }
            <Modal
                className="generic-modal"
                mask={true}
                transitionName=""
                width={'50%'}
                open={open}
                title={modalTitle}
                footer={[null]}
                onCancel={handleCancel}
                style={{width:'100%', display:'flex', flexWrap:'wrap', wordWrap: 'break-word' }}
                wrapClassName="generic-modal-wrapper"
                destroyOnClose={true}     
                
            >
                {modalContent}
            </Modal>
        </div>
    )
        

}

export default GenericModal;