import React, { useEffect, useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useNavigate } from "react-router-dom";
import "../Dashboard.css";
import firebase, { auth, db, logout } from '../services/firebase_auth';
import { query, collection, getDocs, where } from "firebase/firestore";

function Purchase(){
    const [user, loading, error] = useAuthState(auth);
    const [p_uuid, p_setUUID] = useState("");
    const [p_date, p_setDate] = useState("");
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [contact, setContact] = useState("");
    const [po_url, setPOURL] = useState("");
    const navigate = useNavigate(); 

    const [file, setFile] = useState("");
    const [percent, setPercent] = useState(0);
    const [url, setURL] = useState([]);

    const storageRef = ref(storage, `purchases/${file.name}`)

    //Handles change event and update 
    function handleUpdates(event){
        setFile(event.target.files[0]);
    }

    const handleUpload = () => {
        if(!file) {
            alert("Please select a file!");
        }
        const uploadTask = uploadBytesResumable(storageRef, file);

        uploadTask.on(
            "state_changed", (snapshot) => {
                const percent = Math.round(
                    (snapshot.bytesTransferred / snapshot.totalBytes) * 100
                );
                // Determine the progress of the upload
                setPercent(percent)
            }, (err) => console.log(err), () => {
                getDownloadURL(uploadTask.snapshot.ref).then((url) => {
                        console.log(url);
                });
            }
        );
    };

    return(
        <>
            <div>
                <input 
                    type="text"
                    className="login__textBox"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Contact Name"
                />
                <input 
                    type="text"
                    className="login__textBox"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Contact Email"
                />
                <input 
                    type="text"
                    className="login__textBox"
                    value={contact}
                    onChange={(e) => setContact(e.target.value)}
                    placeholder="Contact Number"
                />
                <select name="company" id="company">
                    <option value=""></option>
                </select>
                <input type="file" accept="application/pdf" onChange={handleUpdates}/>
            </div>
            <div>
                <button onClick={handleUpload}>Create Purchase Order</button>
                <p>{percent} % done</p>
            </div>
        </>
    );
}