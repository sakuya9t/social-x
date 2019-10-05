import React, {Component} from 'react';
import './index.css';
import ErrorImage from '../../resources/crypenguin.png';
require('typeface-raleway');

class ErrorPage extends Component{
    render = () => <div className='errorpage-container'>
        <img src={ErrorImage} alt="ErrorImage" />
        <h3>Something wrong happened, please try again later...</h3>
        <h3>Error: {this.props.message}</h3>
    </div>
}
export default ErrorPage;