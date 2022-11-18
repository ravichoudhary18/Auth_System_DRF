import React from 'react'
// import {useNavigate} from 'react-router-dom';


function Dashbord() {

    // const navigate = useNavigate();
    const LogoutHandler = () => {
        localStorage.clear();
        window.location.reload();
        
    }
  return (
    <>
        <div>
            Dashbord
        </div>
        <button onClick={LogoutHandler}>
            Logout
        </button>
    </>
  )
}

export default Dashbord