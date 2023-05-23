import { signInWithGoogle } from "../services/firebase_auth";

import '../App.css';

const Login = () => {
    return (
        <div>
            <button className="button" onClick={signInWithGoogle}><i class="fab fa-google"></i>Sign in with google</button>
        </div>
    )
}

export default Login; 