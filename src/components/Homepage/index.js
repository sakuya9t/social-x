import React, {Component} from 'react';
import './index.css';
import QueryItem from '../QueryItem';
import { Button } from 'react-bootstrap';
import HeaderImg from '../../resources/header.png';

class Homepage extends Component{
    constructor(props){
        super(props);
        this.state = {
            account1 : {
                platformName: "",
                loginChecked: false,
                text: ""
            },
            account2 : {
                platformName: "",
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
                <p className="home-text-center">
                    <img src={HeaderImg} alt="header" width="400" height="250"/>
                </p>
                <div className="home-content-container">
                    <p>Account 1:</p>
                    <QueryItem width="100%" itemkey="1" setData={this.setData.bind(this,1)}/>
                    <p>Account 2:</p>
                    <QueryItem width="100%" itemkey="2" setData={this.setData.bind(this,2)}/>
                    <p className="home-text-center">
                        <Button className="home-submit-btn">Calculate</Button>
                    </p>
                </div>
            </div>
        </>;
    }
}

export default Homepage;