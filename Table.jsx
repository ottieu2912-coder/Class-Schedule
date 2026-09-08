import axios from "axios"

//The Table component displays the schedules of the user.
function Table(props) {
    let quarter = [0, 1, 2];
    //This function sends the name of the schedule and information about the user to the backend for a specific schedule to be deleted.
    async function Del(name) {
        await axios.post("http://127.0.0.1:8000/delete/", {name: name}, {headers: {Authorization: 'Bearer ' + localStorage.getItem("access")}})
        //The webpage automatically reload for the new update to display.
        window.location.reload()
    }
    return (

        <section className="tables">
            <a className="link" onClick={()=>Del(props.calendar.name)} href="">Delete</a>
            <table className="table">
                <thead>
                <tr>
                    <th colSpan={3}>{props.calendar.name}</th>
                </tr>
                <tr>
                    <th scope="col">Quarter 1</th>
                    <th scope="col">Quarter 2</th>
                    <th scope="col">Quarter 3</th>
                </tr>
                </thead>
                <tbody>
                {quarter.map((item, index) => (<tr>
                    <td scope="col" key={(index+1)}>{(props.calendar['schedule'][0].length > item)?props.calendar['schedule'][0][item]: ""}</td>
                    <td scope="col" key={(index+1)*2}>{(props.calendar['schedule'][1].length > item)?props.calendar['schedule'][1][item]: ""}</td>
                    <td scope="col" key={(index+1)*3}>{(props.calendar['schedule'][2].length > item)?props.calendar['schedule'][2][item]: ""}</td>
                </tr>))}
                </tbody>
            </table>
        </section>
    )
}
export default Table;