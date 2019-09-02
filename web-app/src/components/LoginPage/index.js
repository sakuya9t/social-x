import React, {Component} from 'react';
import {uniq} from 'underscore';
import { Form, Button } from 'react-bootstrap';
import './index.css';
import CloseImg from '../../resources/close.png';
import RSA from '../../utils/RSA';

class LoginPage extends Component{

    rsa_module = new RSA();

    closeButtonClicked = () => {
        const {hideLogin} = this.props;
        hideLogin();
    }

    generateForms = () => {
        const {platforms} = this.props;
        return uniq(platforms).map((platformName, index) => 
        <Form className="loginpage-form" key={index} onSubmit={this.onVerify}>
            <Form.Label><h3>Login {platformName}: </h3></Form.Label>

            <Form.Group controlId={`formHorizontalEmail${index}`}>
                <Form.Label className="loginpage-form-label">Account Name</Form.Label>
                <Form.Control type="text" name="username" placeholder="account name or Email" />
            </Form.Group>
        
            <Form.Group controlId={`formHorizontalPassword${index}`}>
                <Form.Label className="loginpage-form-label">Password</Form.Label>
                <Form.Control type="password" name="password" placeholder="Password" />
            </Form.Group>
        
            <Form.Group>
                <Button type="submit">Verify</Button>
            </Form.Group>
        </Form>
        );
    }

    onVerify = (e) => {
        const form = e.target;
        const username = form.username.value;
        //const password = this.rsa_module.encrypt(form.password.value);
        const password = form.password.value;
        console.log(`${username}: ${password}`);
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