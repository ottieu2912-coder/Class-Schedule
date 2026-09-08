import './App.css'
import axios from 'axios'
import {useState, useRef, useEffect} from 'react'
import {useNavigate} from 'react-router-dom'
import Table from './Table'

const token = localStorage.getItem('access')
//The Select component displays the choices for the students to create a schedule.
function Select() {
    //The variable arr is the list of classes that the students select for the schedule.
    let arr = useRef([])
    //Name for the new schedule
    let[name, setName] = useState("Schedule")
    //Error message in case the same name is used for more than one schedule
    let [message, setMessage] = useState("")

    //When the student selects a class, this function verifies whether that class is already selected or not. If already selected, the class is removed, and if not, it is added to the list.
    function addClass(event, name) {
        if(arr.current.includes(name)) arr.current = arr.current.filter((item)=>item!==name); else {
            arr.current.push(name)
        }
        event.target.checked = arr.current.includes(name)
    }

    //Send the list and the token to the backend for the new schedule to be created
    async function createSchedule(){
        if(token !== null) {
            let response = await axios.post('http://127.0.0.1:8000/api/createSchedule/', {
                title: name,
                classes: arr.current
            }, {headers: {Authorization: 'Bearer ' + token}})
            if(response.data['Validity'] === "This name is already taken") setMessage("This name is already taken"); else window.location.reload()
        }
    }

    return (
        <>
            <section className="classSelection">
                <div className="options">
                    <h2 className="classes">Classes</h2>
                    <input onClick={(e)=>addClass(e, "Classical Physics I")}  id="physics1" type="radio"/>
                    <label htmlFor="physics1">Physics 1</label>
                    <input onClick={(e)=>addClass(e, "Classical Physics II")} id="physics2" type="radio"/>
                    <label htmlFor="physics2">Physics 2</label>
                    <input onClick={(e)=>addClass(e, "Classical Physics III")} id="physics3" type="radio"/>
                    <label htmlFor="physics3">Physics 3</label>
                    <input onClick={(e)=>addClass(e, "Multivariable Calc. I")} id="multicalci" type="radio"/>
                    <label htmlFor="multicalci">Multivariable Calc. I</label>
                    <input onClick={(e)=>addClass(e, "Multivariable Calc. II")} id="multicalcii" type="radio"/>
                    <label htmlFor="multicalcii">Multivariable Calc. II</label>
                    <input onClick={(e)=>addClass(e, "Linear Algebra")} id="linearalgebra" type="radio"/>
                    <label htmlFor="linearalgebra">Linear Algebra</label>
                </div>
                <label className="schedulename" htmlFor="name">Name</label>
                <input onChange={(e)=>setName(e.target.value)} id="name" type="text"/>
                <p className="message">{message}</p>
                <button onClick={()=>{window.location.reload()}}>Back</button>
                <button onClick={createSchedule}>Create Schedule</button>
            </section>
        </>
    )
}

//The home page displays the schedules of the user.
function Home(props) {
    const navigate = useNavigate();
    //The variable schedule stores every class schedule of the user for the frontend to display.
    let [schedule, setSchedule] = useState([])
    //The variable select identifies whether the user wants to create a new schedule or not for the Select component to display.
    let[select, setSelect] = useState(false)

    useEffect(()=> {
        //With the token, the frontend receives the list of schedules that the user has from the API of the backend.
        async function getSchedule(token) {
            return await fetch("http://127.0.0.1:8000/api/classSchedule/schedule/", {headers: {Authorization: 'Bearer ' + token}}).then((response) => {return response.json()}).then((data)=>setSchedule(data))
        }
        if(token) getSchedule(token)
    }, [])

    //Navigate the user to the login page
    function login() {
        navigate('/login')
    }

    //When the user logs out, we delete the tokens for the frontend to know that no user is logged in.
    function logout() {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        window.location.reload()
    }

    //Navigate the user to the registration page
    function register() {
        navigate('/register')
    }


    return (
        <>
            <head>
                <title>Class Schedule</title>
            </head>
            <nav>
                <h1>Class Schedule</h1>
                <img alt="" className="uci" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOYPX4WwFR7clVZSMZaxfsHqV3_kBNJHqMyP_F2zbHcDUCfM33ujbMnR0&s=10"/>
                <section className="name">
                    <h1>{props.user.username}</h1>
                    <button onClick={props.user.username==='' ? login : logout}>{props.user.username==='' ? "Login" : "Logout"}</button>
                    <button onClick={register}>Register</button>
                    <h1 onClick={()=>navigate("/info")} className="info">Info</h1>
                </section>
            </nav>
            {schedule.map((calendar, index)=><Table calendar={calendar} key={index}/>)}
            {select && <Select username={props.user.username}/>}
            <section onClick={()=>{setSelect(true)}} className="add">
                <h1>+</h1>
            </section>
        </>
    )
}

export default Home;