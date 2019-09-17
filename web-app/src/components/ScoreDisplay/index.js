import React, {Component} from 'react';
import './index.css';
require('typeface-raleway');

class ScoreDisplay extends Component{
    constructor(props){
        super(props);
        this.state = {
            currValue: 0.0425
        };
    }

    randomValue = () => Math.random().toFixed(4);

    startTimer = () => {
        this.timer = setInterval(
            () => this.setState({
                ...this.state,
                currValue: this.randomValue()
            }), 50
        );
    }

    stopTimer = () => {
        clearInterval(this.timer);
        this.setState({
            ...this.state,
            currValue: this.props.score.toFixed(4)
        });
    }

    componentWillMount(){
        this.startTimer();
        setTimeout(this.stopTimer, 10000);
    }

    render = () => {
        const {currValue} = this.state;
        return <div className='simscore-container'>{currValue}</div>
    }
}
export default ScoreDisplay;