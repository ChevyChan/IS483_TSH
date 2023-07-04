import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { auth, logInWithEmailAndPassword, signInWithGoogle, signInWithMicrosoft } from "../services/firebase_auth";
import { useAuthState } from "react-firebase-hooks/auth";

import '../Login.css';
import axios, { HttpStatusCode } from 'axios';
import { connectStorageEmulator } from "firebase/storage";

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
      // 2 types of user: Employees and Delivery Partners
      // Check for email address. E.g., "@ninjavan.com.sg". Otherwise, set a default group for other generic email addresses
      if (user) {
        fetch('http://localhost:5001/v1/user/get_user_by_id/'+ user.uid, {
          method: 'GET',
          mode: "no-cors",
          headers: {
            'Content-Type': 'application/json',
          }
        })
        .then(response => {
          if(!HttpStatusCode.Ok){
            throw new Error('Bad Request');
          }
        })
        .then(data => {
          console.log(data)

          if(data == null){
            fetch('http://localhost:5001/v1/user/create_user/' + user.uid + '/' + user.email, {
            method: 'POST',
            mode: "no-cors",
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_uuid: user.uid,
              name: user.displayName,
              email: user.email,
              auth_provider: user.providerData[0].providerId,
              // Either Employee or Delivery Partner. To be replaced later
              member_type: "Employee",
              CompanyID: "1",
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
          }else{
            return
          }
        })
        .catch(error => {
          console.log(error)
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