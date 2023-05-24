import React from 'react';

import { auth } from '../services/firebase_auth';

import '../App.css';

const Home = ({ user }) => {
    return (
        <div className='home'>
            <h1>Hello, <span></span> {user.DisplayName}</h1>
            <img src={user.photoURL} alt="" />
            <button className="button signout" onClick={() => auth.signOut()}>Sign out</button>
        </div>
    )
}

export default Home;