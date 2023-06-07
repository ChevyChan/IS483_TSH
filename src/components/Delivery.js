import React, { useEffect, useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useNavigate } from "react-router-dom";
import "../Dashboard.css";
import firebase, { auth, db, logout } from '../services/firebase_auth';
import { query, collection, getDocs, where } from "firebase/firestore";

function Delivery(){
    const [user, loading, error] = useAuthState(auth);
    const [d_uuid, d_setUUID] = useState("");
    const [d_date, d_setDate] = useState("");
    const [d_time, d_setTime] = useState("");
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [contact, setContact] = useState("");
    const [po_url, setPOURL] = useState("")
    const [do_url, setDOURL] = useState("");
    const navigate = useNavigate(); 

    
}
