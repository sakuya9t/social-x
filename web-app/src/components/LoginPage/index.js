import React, {Component} from 'react';
import {uniq} from 'underscore';
import { Form, Button } from 'react-bootstrap';
import './index.css';
import CloseImg from '../../resources/close.png';
import RSA from '../../utils/RSA';

class LoginPage extends Component{
    constructor(props){
        super(props);

        const {platforms} = this.props;
        this.state = {
            platforms: uniq(platforms),
            validated: uniq(platforms).map((platformName) => ({[platformName]: false})).reduce((curr, x) => Object.assign(curr, x), {})
        };
    }

    rsa_module = new RSA();

    closeButtonClicked = () => {
        const {hideLogin} = this.props;
        hideLogin();
    }

    generateForms = () => {
        const {platforms} = this.props;
        return uniq(platforms).map((platformName, index) => 
        <Form className="loginpage-form" key={index} validated={this.state.validated[platformName]} onSubmit={this.onVerify}>
            <Form.Label><h3>Login {platformName}: </h3></Form.Label>
            <input className="loginpage-hidden" type="text" name="platform" defaultValue={platformName} />

            <Form.Group controlId={`formHorizontalEmail${index}`}>
                <Form.Label className="loginpage-form-label">Account Name</Form.Label>
                <Form.Control required type="text" name="username" placeholder="account name or Email" />
                <Form.Control.Feedback type="invalid">Please provide a valid account.</Form.Control.Feedback>
            </Form.Group>
        
            <Form.Group controlId={`formHorizontalPassword${index}`}>
                <Form.Label className="loginpage-form-label">Password</Form.Label>
                <Form.Control required type="password" name="password" placeholder="Password" />
                <Form.Control.Feedback type="invalid">Please provide a valid account.</Form.Control.Feedback>
            </Form.Group>
        
            <Form.Group>
                <Button type="submit">Verify</Button>
            </Form.Group>
        </Form>
        );
    }

    onVerify = (e) => {
        const form = e.target;
        const platform = form.platform.value;
        const username = form.username.value;
        //const password = this.rsa_module.encrypt(form.password.value);
        const password = form.password.value;
        const data = {'platform': platform, 'username': username, 'password': password}
        fetch('http://localhost:5000/login', {
            method: 'POST',
            body: JSON.stringify(data),
            headers:{
                'Content-Type': 'application/json',
            }
        }).then(res => res.json())
        .then(resp => {
            let validated = this.state.validated;
            validated[platform] = resp.result;
            console.log(validated);
            this.setState({
                ...this.state,
                validated: validated
            });
        });
        e.preventDefault();
    }

    render = () => <>
        <div className="loginpage-container">
            <div className="loginpage-content-container">
                <div className="loginpage-close-button" onClick={this.closeButtonClicked}>
                    <img src={CloseImg} alt="close" height="40" width="40"/>
                </div>
                {this.generateForms()}
            </div>
        </div>
    </>
}

export default LoginPage;