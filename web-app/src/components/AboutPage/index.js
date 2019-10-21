import React, {Component} from 'react';
import ReactCanvasNest from 'react-canvas-nest';
import './index.css';
import HeaderImg from '../../resources/logo.png';

class AboutPage extends Component{

    render = () => {
        return <>
            <ReactCanvasNest style={{position:'fixed', opacity:0.2}}/>
            <div className="about-container">
                <p><img src={HeaderImg} alt="logo" width={200} height={200}/></p>
                <div className="about-text">
                    <h1>Project social-X</h1>
                    <p>For the fulfillment of Project:</p>
                    <h3>Linking Users across Social MediaPlatforms</h3>
                    <p>the University of Melbourne</p>
                    <p>November 2019</p>
                </div>
            </div>
        </>
    }
}
export default AboutPage;