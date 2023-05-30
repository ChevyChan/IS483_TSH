// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getDatabase, ref, update, onValue } from "firebase/database";
import { GoogleAuthProvider, getAuth, signInWithPopup, signInWithEmailAndPassword, createUserWithEmailAndPassword, sendPasswordResetEmail, signOut, onAuthStateChanged } from "firebase/auth";
import { getFirestore, query, getDocs, collection, where, addDoc, } from "firebase/firestore";
import { getStorage } from 'firebase/storage';
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
const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
const db = getFirestore(app);

const storage = getStorage(app);

const googleProvider = new GoogleAuthProvider();
//provider.setCustomParameters({ prompt: 'select_account' });

export const signInWithGoogle = async() => {
    try{   
        const res = await signInWithPopup(auth, googleProvider);
        const user = res.user;
        const q = query(collection(db, "users"), where("uid", "==", user.uid));
        const docs = await getDocs(q);
        if (docs.docs.length == 0) {
            await addDoc(collection(db, "users"), {
                uid: user.uid,
                name: user.displayName,
                authProvider: "google",
                email: user.email,
            });
        }
    }catch(err){
        console.error(err);
        alert(err.message);
    }
}

const logInWithEmailAndPassword = async (email, password) => {
    try {
      await signInWithEmailAndPassword(auth, email, password);
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  };
  
  const registerWithEmailAndPassword = async (name, email, password) => {
    try {
      const res = await createUserWithEmailAndPassword(auth, email, password);
      const user = res.user;
      await addDoc(collection(db, "users"), {
        uid: user.uid,
        name,
        authProvider: "local",
        email,
      });
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  };
  
  const sendPasswordReset = async (email) => {
    try {
      await sendPasswordResetEmail(auth, email);
      alert("Password reset link sent!");
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  };
  
  const logout = () => {
    signOut(auth);
  };

export {
    db, 
    logInWithEmailAndPassword,
    registerWithEmailAndPassword,
    sendPasswordReset,
    logout,
    storage
};



// function signInWithGoogle(){
//     const auth = getAuth();
//     signInWithPopup(auth, provider)
//         .then((result) => {
//             // This gives you a Google Access Token. You can use it to access the Google API
//             const credential = GoogleAuthProvider.credentialFromResult(result);
//             const token = credential.accessToken;
//             // The signed-in user info
//             const user = result.user;
//             // Additional Info, if needed
//             //const addInfo = result.getAdditionalUserInfo(result);

//             // Load to the main page (Dashboard)
//             // window.onload("Dashboard")

//         }).catch((error) => {
//             const errorCode = error.code;
//             const errorMessage = error.message;
//             // The email of the user's account used
//             const email = error.customData.email;
//             // The AuthCredential type that was used.
//             const credential = GoogleAuthProvider.credentialFromError(error);
//         });
//     }
    
// // Put this function at the other pages. Not for login page
// function signOutFromWeb(){
//     const auth = getAuth();
//     signOut(auth).then(() => {
//         // Sign out successfully.
//         //window.onload("LoginPage")
//     }).catch((error) => {
//         //An error happened.
//         const errCode = error.code;
//         const errMsg = error.message;
//     })
// }