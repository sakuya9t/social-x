import React, {Component} from 'react';
import './index.css';
require('typeface-raleway');

class ScoreBar extends Component{
    constructor(props){
        super(props);
        this.state = {
            currWidth: 0
        };
    }

    count = 0;

    startTimer = () => {
        const {score, delay} = this.props;
        this.timer = setInterval(
            () => {
                this.setState({
                    ...this.state,
                    currWidth: `${this.count / (delay) * score}%`
                });
                this.count++;
            }, 20
        );
    }

    stopTimer = () => {
        clearInterval(this.timer);
    }

    componentDidMount = () => {
        const {delay} = this.props;
        this.startTimer();
        setTimeout(this.stopTimer, delay * 1000);
    }

    render = () => {
        const {score} = this.props;
        const {currWidth} = this.state;
        return <div className = 'scorebar-container'>
            <div className='scorebar-indicator' style={{width: currWidth}}/>
            <span className='scorebar-score'>{score}</span>
        </div>
    }
}
export default ScoreBar;