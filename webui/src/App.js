import './App.css';
import { useEffect } from 'react';
import AppContent from './components/pages/AppContent/AppContent';

function App() {

  useEffect(()=>{
    document.title = "Mr Know All"
  }, [])

  return (
    <div className="App">
      <AppContent />
    </div>
  );
}

export default App;
