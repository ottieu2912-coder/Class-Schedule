import axios from 'axios'
import {useState} from 'react'
import {useNavigate} from "react-router-dom";
import "./Login.css"


function Login(props) {
    const navigate = useNavigate();
    //Error message for the user when the submitted information is incorrect
    let [message, setMessage] = useState('')

    async function handleLogin(e) {
        //Prevent the default reload of the webpage for the API's information to be processed
        e.preventDefault()
        try {
            //The frontend send the username and password for the backend to validate.
            const response = await axios.post("http://127.0.0.1:8000/login/", { username: props.user.username, password: props.user.password })
            const {access, refresh} = response.data
            //The access and refresh tokens are stored for authentication.
            localStorage.setItem('access', access)
            localStorage.setItem('refresh', refresh)
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access
            setMessage("Logged in")
            //Send the user back to the Home page
            navigate("/")
        } catch {
            //In case, the information is not validated, the frontend lets the user know that the username or password is invalid.
            alert("Invalid username or password")
            setMessage("Wrong password or username")
        }
    }

    return (
        <>
            <form onSubmit={handleLogin}>
                <img alt="" className="ucilogin" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOYPX4WwFR7clVZSMZaxfsHqV3_kBNJHqMyP_F2zbHcDUCfM33ujbMnR0&s=10"/>
                <input className="input" type="text" placeholder="Username" onChange={(event)=>props.userUpdateUsername(event.target.value)}/>
                <input className="input" type="password" placeholder="Password" onChange={(event)=>props.userUpdatePassword(event.target.value)}/>
                <input className="input" id="submit" type="submit" value="Login" />
                <h3>{message}</h3>
            </form>
        </>
    )
}

function Registration(props) {
    //The frontend create an entire new set of password, email, and username for the new user.
    let [message, setMessage] = useState('')
    let [username, setUsername] = useState('')
    let [password, setPassword] = useState('')
    let [email, setEmail] = useState('')

    async function register() {
        //When registered, the frontend sends data to the backend for the new user's information to be stored.
        let response = await axios.post('http://127.0.0.1:8000/register/', {email: email, password: password, username: username})
        //Message about the registration's status
        setMessage(response.data.Valid)
        if(message === "Registration Success"){
            props.userUpdateUsername(username)
            props.userUpdatePassword(password)
            try {
                //Like the login page, when the user is registered, we get the access and refresh tokens from the backend for validation.
                const response = await axios.post("http://127.0.0.1:8000/login/", { username: username, password: password })
                const {access, refresh} = response.data
                localStorage.setItem('access', access)
                localStorage.setItem('refresh', refresh)
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access
            } catch {
                alert("Invalid username or password")
            }
        }
    }

    return (
        <>
            <form>
                <img alt="" className="ucilogin" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOYPX4WwFR7clVZSMZaxfsHqV3_kBNJHqMyP_F2zbHcDUCfM33ujbMnR0&s=10"/>
                <input className="input" type="text" placeholder="Username" onChange={(event)=>setUsername(event.target.value)}/>
                <input className="input" type="text" placeholder="Email" onChange={(event)=>setEmail(event.target.value)}/>
                <input className="input" type="password" placeholder="Password" onChange={(event)=>setPassword(event.target.value)}/>
                <input className="input" id="submit" type="submit" value="Register" onClick={register} />
                <h3>{message}</h3>
            </form>
        </>
    )
}

export {Registration, Login};