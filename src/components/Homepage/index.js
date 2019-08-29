import React, {Component} from 'react';
import './index.css';
import QueryItem from '../QueryItem';
import { Button } from 'react-bootstrap';

class Homepage extends Component{

    render(){
        return <>
            <div className="home-container">
                <p>Account 1:</p>
                <QueryItem width="100%"/>
                <p>Account 2:</p>
                <QueryItem width="100%"/>
                <Button className="home-submit-btn">Calculate</Button>
            </div>
        </>;
    }
}

export default Homepage;