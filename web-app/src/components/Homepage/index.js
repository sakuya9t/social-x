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
        const data = {
            account1: {
                platform: account1.platformName,
                account: account1.text
            }, 
            account2: {
                platform: account2.platformName,
                account: account2.text
            }};

        // fetch('http://localhost:5000/query', {
        //     method: 'POST',
        //     body: JSON.stringify(data),
        //     headers:{
        //         'Content-Type': 'application/json',
        //     }
        // }).then(res => res.text())
        // .then(res => console.log(res));

        // test data for ui
        let resdata = {
            doc_id: '5475aa38048c626ea3f4b0cc53000528',
            result: {
                score: 0.687509,
                columns: {
                    score: 'Overall Similarity',
                    username: 'User Name',
                    profileImage: 'Profile Image',
                    self_desc: 'Text in Self Description',
                    desc_overlap_url_count: 'URL in Self Description',
                    readability: 'Writing Style (Readability)',
                    tea: 'Writing Style (Tea)',
                    post_text: 'Text in Posts',
                    uclassify: 'UClassify Similarity'
                },
                vector:{
                    username: 0.1333333333333333,
                    profileImage: 0.5357508659362793,
                    self_desc: 0.23544350266456604,
                    desc_overlap_url_count: 0,
                    writing_style: {
                    readability: 0.8307164884251507
                    },
                    post_text: 0.3679984211921692,
                    uclassify: 0.044702274925621885,
                    label: 0
                }
              }
        };
        // test data for ui end

        this.setState({
            ...this.state,
            result: resdata.result,
            showResult: true,
            resultId: resdata.doc_id
        });

        animateScroll.scrollToBottom();
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

                {showResult ? <ResultPage waiting={waitingResult} data={JSON.stringify(result)}/> : null}
            </div>
            {this.LoginPage.apply()}
        </>;
    }
}

export default Homepage;