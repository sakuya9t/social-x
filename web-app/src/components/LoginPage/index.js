import React, {Component} from 'react';
import {uniq} from 'underscore';
import { Form, Button } from 'react-bootstrap';
import './index.css';
import CloseImg from '../../resources/close.png';

class LoginPage extends Component{
    closeButtonClicked = () => {
        const {hideLogin} = this.props;
        hideLogin();
    }

    generateForms = () => {
        const {platforms} = this.props;
        return uniq(platforms).map((platformName) => 
        <Form className="loginpage-form">
            <Form.Label><h3>Login {platformName}: </h3></Form.Label>

            <Form.Group controlId="formHorizontalEmail">
                <Form.Label className="loginpage-form-label">Account Name</Form.Label>
                <Form.Control type="text" placeholder="account name or Email" />
            </Form.Group>
        
            <Form.Group controlId="formHorizontalPassword">
                <Form.Label className="loginpage-form-label">Password</Form.Label>
                <Form.Control type="password" placeholder="Password" />
            </Form.Group>
        
            <Form.Group>
                <Button type="submit">Validate</Button>
            </Form.Group>
        </Form>
        );
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