import React, {Component} from 'react';
import './index.css';
import { BounceLoader } from 'react-spinners';
import ScoreDisplay from '../ScoreDisplay';

class ResultPage extends  Component{
    constructor(props) {
        super(props);
        this.state = {
            loading: true
        };
    }

    displayRows = (columns, vector) => {
        for(let key of Object.keys(vector)){
            if(columns[key]){
                console.log(columns[key]);
            }
        }
    } 

    render(){
        const {data, waiting} = this.props;
        if(waiting){
            return (
                <div className='resultpage-container'>
                    <div className='sweet-loading icon-container'>
                        <BounceLoader
                            className='icon-waiting'
                            sizeUnit={"px"}
                            size={150}
                            color={'#37B5FF'}
                            loading={this.state.loading}
                        />
                    </div> 
                    <h2 className='resultpage-textcenter'>Fetching data, please stand by...</h2>
                </div>
              );
        }
        else{
            const jsondata = JSON.parse(data);
            const {score, columns, vector} = jsondata;
            this.displayRows(columns, vector);
            return (
                <div className='resultpage-container'>
                    <div className='reaultpage-overall-indicator'>The Overall Similarity Score is: </div>
                    <ScoreDisplay score={score} delay={3} />
                    <ul></ul>
                    {data}
                </div>
            );
        }
    }
}

export default ResultPage;