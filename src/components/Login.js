import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { auth, logInWithEmailAndPassword, signInWithGoogle, signInWithMicrosoft } from "../services/firebase_auth";
import { useAuthState } from "react-firebase-hooks/auth";

import '../Login.css';
import axios, { HttpStatusCode } from 'axios';

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [user, loading, error] = useAuthState(auth);
    const [postData, setPostData] = useState({body: ''})
    const navigate = useNavigate();
    useEffect(() => {
      if (loading) {
        // maybe trigger a loading screen
        return;
      }
      if (user) {
        fetch('http://localhost:5001/v1/user/create_user/' + user.uid + '/' + user.email, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: user.displayName,
            email: user.email,
            auth_provider: user.providerData[0].providerId,
            member_type: "Employee",
            "company_name": "Tong Tah",
            "company_address": "123 Adam Rd #01-01",
            "company_contact": "63219876",
            "company_email": "support@tongtah.sg"
          })
        })
          .then(response => {
            if(!HttpStatusCode.Ok){ 
              throw new Error('Bad Request');
            }
          })
          .then(data => {
            // Handle the response data
            console.log(data);
          })
          .catch(error => {
            //Handle any errors
            console.error(error);
          })

        navigate("/dashboard");
      }
    }, [user, loading]);
    return (
      <div className="login">
        <div className="login__container">
          <input
            type="text"
            className="login__textBox"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="E-mail Address"
          />
          <input
            type="password"
            className="login__textBox"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
          <button
            className="login__btn"
            onClick={() => logInWithEmailAndPassword(email, password)}
          >
            Login
          </button>
          <button className="login__btn login__google" onClick={signInWithGoogle}>
            Login with Google
          </button>
          <button className="login__btn login__microsoft" onClick={signInWithMicrosoft}>
            Login with Microsoft
          </button>
          <div>
            <Link to="/reset">Forgot Password</Link>
          </div>
          <div>
            Don't have an account? <Link to="/register">Register</Link> now.
          </div>
        </div>
      </div>
    );
  }

export default Login; 