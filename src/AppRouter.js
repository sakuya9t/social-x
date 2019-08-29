import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

const Index = <h2>Home</h2>;
const About = <h2>About</h2>;

function AppRouter() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/about/">About</Link>
            </li>
          </ul>
        </nav>

        <Route path="/" exact component={Index} />
        <Route path="/about/" component={About} />
      </div>
    </Router>
  );
}

export default AppRouter;