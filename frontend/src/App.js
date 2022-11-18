import React, {Fragment} from 'react';
import Login from './components/authentication/Login';
import Dashbord from './components/Dashbord/Dashbord';
import './App.css';

function App() {
  return (
    <>
    {
      localStorage.length > 0 ? <Dashbord /> : <Login />
    }
    </>
  );
}

export default App;
