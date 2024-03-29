import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import './Header.css';
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { useUser } from '../context/UserContext';


const Header = () => {

  const { isLoggedIn } = useUser();

  return (
    <div>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Navbar.Brand>Sensor Center</Navbar.Brand>
        {isLoggedIn && 
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ml-auto">
            <Link className="nav-link" to="/home">Inici</Link>
            <Link className="nav-link" to="/data">Dades</Link>
            <Link className="nav-link" to="/parameters">Paràmetres</Link>
            <Link className="nav-link" to="/profile"><FontAwesomeIcon icon="circle-user" size='2xl' style={{ color: "#FFFFFF" }} /></Link>
          </Nav>
        </Navbar.Collapse> }
        
      </Navbar>
    </div>
  );
};

export default Header;

