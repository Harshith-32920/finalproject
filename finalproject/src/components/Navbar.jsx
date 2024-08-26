import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
    return (
        <nav className="navbar">
            <ul className="navbar-links">
                
                <li>
                    <Link to="/">Home</Link>
                </li>
                {/* <li>
                    <Link to="/about">About</Link>
                </li> */}
                <li>
                    <Link to="/crud">Tasks</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
