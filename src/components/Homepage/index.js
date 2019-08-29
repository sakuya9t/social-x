import React, {Component} from 'react';
import './index.css';
import QueryItem from '../QueryItem';
import { Button } from 'react-bootstrap';

class Homepage extends Component{
    constructor(props){
        super(props);
        this.state = {
            account1 : {
                loginChecked: false,
                text: ""
            },
            account2 : {
                loginChecked: false,
                text: ""
            }
        }
    }

    setData = (id, source) => {
        let target = {};
        Object.assign(target, source);
        if(id === 1) {
            this.setState({
                ...this.state,
                account1: target
            });
        }
        else if(id === 2) {
            this.setState({
                ...this.state,
                account2: target
            });
        }
    }

    sendRequest = () => {

    }

    render(){
        return <>
            <div className="home-container">
                <p>Account 1:</p>
                <QueryItem width="100%" itemkey="1" setData={this.setData.bind(this,1)}/>
                <p>Account 2:</p>
                <QueryItem width="100%" itemkey="2" setData={this.setData.bind(this,2)}/>
                <Button className="home-submit-btn">Calculate</Button>
            </div>
        </>;
    }
}

export default Homepage;