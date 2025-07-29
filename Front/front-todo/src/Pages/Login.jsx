import React from "react";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const navigate = useNavigate();

  return (
    <div className="login-container-general">
        <div className="login-container-form">
            <h1 classname="login-title">Login</h1>
            <form className="login-form">
                <div className="login-input-container">
                    <label htmlFor="username">Username</label>
                    <input type="text" id="username" name="username" required />
                </div>
                <div className="login-input-container">
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" name="password" required />
                </div>
                <button type="submit" className="login-button">Login</button>
            </form>
        </div>
    </div>
  );
};

export default LoginPage;