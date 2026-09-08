import './App.css'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Home from './Home'
import {Login, Registration} from "./Login.jsx";
import Info from "./Info.jsx"
import {useState, useEffect} from "react";
import axios from "axios"


function App() {
  //Prepare the variables for user's information such as username or password to display
  let [user, setUser] = useState({username: '', password: ''})

  //function to update username and password when the user's account changes
  function updateUsername(value) {
    setUser({username: value, password: user.password})
  }
  function updatePassword(value) {
    setUser({username: user.username, password: value})
  }

  //Retrieve the access token from the backend to authenticate the user
  const getUser = (token)=>{return axios.get("http://127.0.0.1:8000/getUser/", {headers: {Authorization: 'Bearer ' + token}}).then((res) => {
    updateUsername(res.data.username)
  })}

  //Use the refresh token to get a new valid access token when the old access token expires
  async function refresh(token) {
    token = await axios.post("http://127.0.0.1:8000/api/refresh/", {refresh: localStorage.getItem("refresh")})
    return token.data['access']
  }

  //When the website mounts, the frontend receives the information about the user through the access token.
  useEffect(()=>{
    let token = localStorage.getItem('access')
    //If the token exists, the user is logged in. However, in case the frontend catches a 401 unauthorized error, which means that the access token expires, the frontend sends the refresh token to the backend and gets a new valid access token.
    if(token) getUser(token).catch(()=>{
        token = refresh(token).then((res)=>{localStorage.setItem('access', res)})
    })
  },[])

  return(
    //Assign the routes to different components
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login user={user} userUpdateUsername={updateUsername} userUpdatePassword={updatePassword}/>}/>
          <Route path="/register" element={<Registration user={user} userUpdateUsername={updateUsername} userUpdatePassword={updatePassword}/>}/>
          <Route path="/" element={<Home user={user}/>}/>
          <Route path="/info" element={<Info/>}/>
        </Routes>
      </BrowserRouter>
    </>
  )
}


export default App
