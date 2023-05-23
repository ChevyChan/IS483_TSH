// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
import { getDatabase, ref, update, onValue } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-auth.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDgLtAF9kci3YsoPnkl21pHe-BkwbUR7Gs",
    authDomain: "is483-tsh.firebaseapp.com",
    projectId: "is483-tsh",
    storageBucket: "is483-tsh.appspot.com",
    messagingSenderId: "961210053273",
    appId: "1:961210053273:web:aced8e09c7596af2a43e08",
    measurementId: "G-NQL1BXQZD9"
};

// Initialize Firebase
firebaseConfig.initializeApp(firebaseConfig);

export const auth = firebase.auth();

const provider = new firebase.auth.GoogleAuthProvider();
provider.setCustomParameters({ prompt: 'select_account' });

export const signInWithGoogle = () => auth.signInWithPopup(provider)

export default firebase_auth;



function signInWithGoogle(){
    const auth = getAuth();
    signInWithPopup(auth, provider)
        .then((result) => {
            // This gives you a Google Access Token. You can use it to access the Google API
            const credential = GoogleAuthProvider.credentialFromResult(result);
            const token = credential.accessToken;
            // The signed-in user info
            const user = result.user;
            // Additional Info, if needed
            //const addInfo = result.getAdditionalUserInfo(result);

            // Load to the main page (Dashboard)
            // window.onload("Dashboard")

        }).catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            // The email of the user's account used
            const email = error.customData.email;
            // The AuthCredential type that was used.
            const credential = GoogleAuthProvider.credentialFromError(error);
        });
    }
    
// Put this function at the other pages. Not for login page
function signOutFromWeb(){
    const auth = getAuth();
    signOut(auth).then(() => {
        // Sign out successfully.
        //window.onload("LoginPage")
    }).catch((error) => {
        //An error happened.
        const errCode = error.code;
        const errMsg = error.message;
    })
}