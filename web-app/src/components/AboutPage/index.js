import React, {Component} from 'react';

class AboutPage extends Component{
    constructor(props){
        super(props);
        this.state = {
            abc: "123"
        }
    }

    testClick = () => {
        this.setState({
            ...this.state,
            abc: "456"
        }, () => {
            setTimeout(() => this.setState({
                ...this.state,
                abc: "789"
            }), 6000);
        });
    }

    render = () => {
        return <>
            <button onClick={this.testClick}>abc</button>
            {this.state.abc}
        </>
    }
}
export default AboutPage;