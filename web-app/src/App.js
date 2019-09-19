import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { Navbar, Nav } from 'react-bootstrap';
import Homepage from "./components/Homepage";
import Aboutpage from "./components/AboutPage";
import LogoImg from './resources/logo.png';

function App() {
  return (
    <Router>
      <div>
        <Header />
        <Route exact path="/" component={Home} />
        <Route path="/about" component={About} />
      </div>
    </Router>
  );
}

const Home = () => <Homepage />;

const About = () => <Aboutpage />;

const Header= () => 
    <Navbar bg="light" expand="lg">
      <Navbar.Brand href="/">
        <img
          src={LogoImg}
          width="32"
          height="32"
          className="d-inline-block align-top"
          alt="React Bootstrap logo"
        />
        <span>Social X</span>
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="/">Home</Nav.Link>
        </Nav>
        <Nav>
        <Nav.Link href="https://github.com/sakuya9t/social-x">SourceCode</Nav.Link>
          <Nav.Link href="/about/">About</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>;

export default App;