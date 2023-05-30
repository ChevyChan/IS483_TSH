import {useState} from 'react'
import {storage} from '../services/firebase_auth.js'
import {ref, uploadBytesResumable, getDownloadURL, listAll, list} from 'firebase/storage'
import { async, validateArgCount } from '@firebase/util';
import { HttpStatusCode } from 'axios';

function UploadDocument() {
    const [file, setFile] = useState("");
    const [percent, setPercent] = useState(0);
    const [url, setURL] = useState([]);

    const storageRef = ref(storage, `files/${file.name}`)

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

    const handleListing = async () => {
        const storageRef = await ref(storage, "files/");

        listAll(storageRef).then((result) => {
            // Check the url of the file(s)
            result.items.forEach((itemRef) => {
                getDownloadURL(itemRef).then(results => {
                    setURL(url => [...url, results]);
                })
            });

            console.log(url);
            return url;
        })
        .catch((error) => {
            console.log(error);
        });
    };

    return(
        <>
            <div>
                <input type="file" accept="application/pdf" onChange={handleUpdates}/>
                <button onClick={handleUpload}>Upload to Firebase</button>
                <p>{percent} % done</p>
            </div>

            <div>
                <button onClick={handleListing}>List Documents</button> 
                <div>
                    <ol>
                        {url.map(urls => <li>{urls}</li> )}
                    </ol>
                </div>  
            </div>
        </>
    );
}

export default UploadDocument;