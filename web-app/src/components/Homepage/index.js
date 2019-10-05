import React, {Component} from 'react';
import './index.css';
import QueryItem from '../QueryItem';
import LoginPage from '../LoginPage';
import ResultPage from '../ResultPage';
import { Button } from 'react-bootstrap';
import ReactCanvasNest from 'react-canvas-nest';
import {animateScroll} from 'react-scroll';
import HeaderImg from '../../resources/header.png';

class Homepage extends Component{
    constructor(props){
        super(props);
        this.state = {
            account1 : {
                platformName: "Select Platform..",
                loginChecked: false,
                text: ""
            },
            account2 : {
                platformName: "Select Platform..",
                loginChecked: false,
                text: ""
            },
            displayLoginWindow: false,
            displayLoginPlatforms: [],
            result: {},
            resultId: null,
            waitingResult: false,
            showResult: false
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
        const {account1, account2} = this.state;
        const reqdata = {
            account1: {
                platform: account1.platformName.toLowerCase(),
                account: account1.text
            }, 
            account2: {
                platform: account2.platformName.toLowerCase(),
                account: account2.text
            }};

        this.setState({
            ...this.state,
            showResult: true,
            waitingResult: true
        }, () => {
            animateScroll.scrollToBottom();
            fetch('http://localhost:5000/query', {
                method: 'POST',
                body: JSON.stringify(reqdata),
                headers:{
                    'Content-Type': 'application/json',
                }
            }).then(res => res.json())
            .then(resdata => {
                this.setState({
                    ...this.state,
                    waitingResult: false,
                    result: resdata,
                    resultId: resdata.doc_id
                });
            });
        });
    }

    submit = () => {
        const {account1, account2} = this.state;
        let platforms = [];
        if([account1.platformName, account2.platformName].includes("Select Platform..")){
            alert("Please select a social media platform.");
            return;
        }
        if(!account1.loginChecked && !account2.loginChecked && account1.text === "" && account2.text === ""){
            alert("Please input an account name.");
            return;
        }
        if(account1.loginChecked){
            platforms.push(account1.platformName);
        }
        if(account2.loginChecked){
            platforms.push(account2.platformName);
        }

        if(!account1.loginChecked && !account2.loginChecked){
            this.sendRequest();
        }

        else{
            this.setState({
                ...this.state,
                displayLoginPlatforms: platforms,
                displayLoginWindow: platforms.length > 0
            });
        }
    }

    hideLogin = () => {
        this.setState({
            ...this.state,
            displayLoginWindow: false
        });
    }

    LoginPage = () => this.state.displayLoginWindow ? <LoginPage hideLogin={this.hideLogin} 
                                                                 platforms={this.state.displayLoginPlatforms} 
                                                                 sendRequest = {this.sendRequest} /> : null;

    render(){
        const {waitingResult, showResult, result} = this.state;
        return <>
            <ReactCanvasNest style={{position:'fixed', opacity:0.2}}/>
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
                        <Button className="home-submit-btn" onClick={this.submit}>Calculate</Button>
                    </p>
                </div>
            </div>
            {showResult ? <ResultPage waiting={waitingResult} data={JSON.stringify(result)}/> : null}
            {this.LoginPage.apply()}
        </>;
    }
}

export default Homepage;