import React, { useState } from 'react';
import { Button, Modal } from 'antd';
import Signup from './Signup';
import GenericModal from '../../common/Modal/GenericModal';


const AuthModal = () => {
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [value, setValue] = React.useState(0);

 //handle open
  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
  };


  //handle close
  const handleCancel = () => {
    setIsModalOpen(false);
  };


  return (
    <>
      
      <GenericModal 
            open={isModalOpen} 
            setOpen={setIsModalOpen}
            loading={null}
            setLoading={null} 
            onCancel={handleCancel}
            modalButtonText="Sign up"
            modalTitle={"Login modal"}
            modalContent={<Signup/>}            
        />    
    {/*}
      <Modal title="Basic Modal" o open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
        <Signup/>
      </Modal>
    */}
    </>
  );
};

export default AuthModal;