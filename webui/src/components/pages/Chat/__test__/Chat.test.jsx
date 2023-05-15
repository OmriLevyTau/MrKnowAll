import { fireEvent, render, screen, waitFor, act } from '@testing-library/react';
import Chat from "../Chat";
import AppContext from '../../AppContent/AppContext';
import { BrowserRouter } from 'react-router-dom';



describe("Test User Input and Server Response for Chat Component", ()=>{

    beforeEach(() => {
      render(
        <AppContext>
          <BrowserRouter>
            <Chat />
          </BrowserRouter>
        </AppContext>
      );
    });

    it('should get user input, disable button on submit and clear input, finally enable button', async () => {
      const userInput = screen.getByRole('textbox');
      const sendBtn = screen.getByTestId('send-message-button');
  
      act(() => {
        fireEvent.change(userInput, { target: { value: "Hello ChatGPT!" } });
      });
 
      act(() => {
        fireEvent.click(sendBtn);
      });
  
      expect(sendBtn).toBeDisabled();
      expect(userInput.value).toBe("");
    
      await waitFor(() => {
        expect(sendBtn).toBeEnabled();
      }, { timeout: 4000 });
    });

    it('should not send an empty message', async () => {
      const sendBtn = screen.getByTestId('send-message-button');
  
      act(() => {
        fireEvent.click(sendBtn);
      });
      await waitFor(() => expect(sendBtn).not.toBeDisabled());
    });

    it('should display user message ', async () => {
      const userInput = screen.getByRole('textbox');
      const sendBtn = screen.getByTestId('send-message-button');
  
      act(() => {
        fireEvent.change(userInput, { target: { value: "Hello ChatGPT!" } });
      });
  
       act(() => {
        fireEvent.click(sendBtn);
      });

      await waitFor(() => {
        expect(screen.getByText("Hello ChatGPT!")).toBeInTheDocument();
      }, { timeout: 4000 });
  
    });
  
    it('should display chatgpt response', async () => {
        const userInput = screen.getByRole('textbox');
        const sendBtn = screen.getByTestId('send-message-button');

        act(()=>{
          fireEvent.change(userInput, {target:{value: "Hello ChatGPT!"}});
        });        
        act(()=>{
          fireEvent.click(sendBtn);
        });        
        
        await waitFor(()=>{
          expect(screen.getByText(/generic/i)).toBeInTheDocument();
        }, {timeout: 4000})
      });

});


