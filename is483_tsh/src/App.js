import { useState, useEffect } from 'react';

import Login from './components/Login';
import Home from './components/Home';
import firebase_auth from './services/firebase_auth';

import './App.css';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    firebase_auth().onAuthStateChanged(user => {
      setUser(user);
    })
  }, [])

  console.log(user);

  return (
    <div className="app">
      {user? <Home user={user} /> : <GoogleLogin />}
    </div>
  );
}

export default App;
