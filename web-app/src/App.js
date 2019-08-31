import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { Navbar, Nav } from 'react-bootstrap';
import Homepage from "./components/Homepage";

function App() {
  return (
    <Router>
      <div>
        <Header />

        <Route exact path="/" component={Home} />
        <Route path="/source" component={Source} />
        <Route path="/about" component={About} />
      </div>
    </Router>
  );
}

const Home = () => <Homepage />;

const About = () => <h2>About</h2>;

const Source = () => <h2>SourceCode</h2>;

const Header= () => 
    <Navbar bg="light" expand="lg">
      <Navbar.Brand href="/">
        <span>Social X</span>
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="/">Home</Nav.Link>
        </Nav>
        <Nav>
        <Nav.Link href="/source/">SourceCode</Nav.Link>
          <Nav.Link href="/about/">About</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>;

export default App;