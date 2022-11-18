import axios from 'axios';
import React, { useState } from 'react';
import styles from './Login.module.css';
function Login() {

    const [userFileld, setuserField] = useState('');
    const [passwordFileld, setpasswordField] = useState('');
    const [error, seterror] = useState('');

    const loginHandler = (e) => {
        e.preventDefault();
        const data = new FormData();
        data.append('username', userFileld)
        data.append('password', passwordFileld)
        axios.post('http://localhost:8000/api/accounts/login/', data)
        .then(response => {
            if (response.status === 200) {
                localStorage.setItem("accessToken", response.data.UserToken.access);
                localStorage.setItem("refreshToken", response.data.UserToken.refresh);
                localStorage.setItem("username", response.data.UserInfo.username);
                localStorage.setItem("role", response.data.UserInfo.role);
                window.location.reload();
            }
        })
        .catch(err => {
            seterror(err.response.data.non_field_errors[0]);
        })
    }

  return (
    <>
    <h1>Login</h1>
    <form onSubmit={loginHandler}>
        <label 
            htmlFor="username">
            Email or Username
        </label><br />
        <input 
            type="text" 
            name="username" 
            onChange={
                (e) => {setuserField(e.target.value)}
            } /> <br />
        <label 
            htmlFor="password">
            Password
        </label><br />
        <input 
            type="password" 
            name="password" 
            onChange={
                (e) => {setpasswordField(e.target.value)}
            } 
        /><br />
        <p className={styles.error_messages}>
            {error}
        </p>
         <br />
        <button type="submit">login</button>
    </form>
    </>
  )
}

export default Login