import React, {Component} from 'react';
import { faThumbsUp, faThumbsDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import './index.css';

class Feedback extends Component{
    constructor(props){
        super(props);
        this.state = {
            rated: false
        }
    }

    recordFeedback = (value) => {
        const {doc_id} = this.props;
        const reqdata = {
            doc_id: doc_id,
            feedback: value ? 1 : 0
        };
        fetch('http://localhost:5000/feedback', {
            method: 'POST',
            body: JSON.stringify(reqdata),
            headers:{
                'Content-Type': 'application/json',
            }
        }).then(() => this.setState({
            ...this.state,
            rated: true
        }));
        
    }

    feedbackArea = <section className="rating-area align-center">
                    <div className="thumbs-up-circle align-center transition-fast" onClick={() => this.recordFeedback(true)}>
                        <span className="thumbs-up transition-fast"><FontAwesomeIcon icon={faThumbsUp} /></span>
                    </div>
                    <div className="thumbs-up-circle align-center transition-fast" onClick={() => this.recordFeedback(false)}>
                        <span className="thumbs-down transition-fast"><FontAwesomeIcon icon={faThumbsDown} /></span>
                    </div>
                </section>

    render = () => <div className="feedback-container">
        {this.state.rated ? <div className='feedback-text'>Thank you for your feedback!</div>: this.feedbackArea}
    </div>
}
export default Feedback;