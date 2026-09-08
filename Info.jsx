import {useNavigate} from "react-router-dom";

//The Info page displays information about each class.
function Info() {
    const navigate = useNavigate();
    function Back() {
        navigate('/');
    }
    return (
        <>
            <a href="" onClick={Back} className="back">Back</a>
            <h1>Classes</h1>
            <h3>Prerequisite: requirements that must be fulfilled before taking the class </h3>
            <h3>Corequisites: requirements that must be fulfilled while taking the class</h3>
            <h2>Classical Physics I</h2>
            <p>Detail: Topics include force, energy, momentum, rotation, and gravity.
            </p>
            <h3>Prerequisites: Math Placement</h3>
            <h2>Classical Physics II</h2>
            <p>Detail: Electricity and magnetism.
            </p>
            <h3>Prerequisites: Classical Physics I</h3>
            <h3>Corequisites: Multivariable Calculus I</h3>
            <h2>Classical Physics III</h2>
            <p>Detail: Fluids; oscillations; waves; and optics.
            </p>
            <h3>Prerequisites: Classical Physics II</h3>
            <h2>Multivariable Calculus I</h2>
            <p>Detail: Differential and integral calculus of real-valued functions of several real variables, including applications. Polar coordinates.</p>
            <h3>Prerequisites: Math Placement</h3>
            <h3>Corequisites: Classical Physics II</h3>
            <h2>Multivariable Calculus II</h2>
            <p>Detail: The differential and integral calculus of vector-valued functions. Implicit and inverse function theorems. Line and surface integrals, divergence and curl, theorems of Greens, Gauss, and Stokes.
            </p>
            <h3>Prerequisites: Multivariable Calculus I</h3>
            <h2>Linear Algebra</h2>
            <p>Detail: Systems of linear equations, matrix operations, determinants, eigenvalues and eigenvectors, vector spaces, subspaces, and dimension.
            </p>
            <h3>Prerequisites: Math Placement</h3>
        </>
    )
}

export default Info;