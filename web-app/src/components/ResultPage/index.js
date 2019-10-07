import React, {Component} from 'react';
import './index.css';
import { BounceLoader } from 'react-spinners';
import ErrorPage from '../ErrorPage';
import ScoreDisplay from '../ScoreDisplay';
import ScoreBar from '../ScoreBar';
import Feedback from '../Feedback';
const _ = require('underscore');


const flattenObject = (ob) => {
    let toReturn = {};

    Object.keys(ob).forEach((key) => {
        if((typeof ob[key]) == 'object' && ob[key] !== null){
            const flatObject = flattenObject(ob[key]);
            Object.keys(flatObject).forEach((subkey) => {
                flatObject.hasOwnProperty(subkey) && (toReturn[subkey] = flatObject[subkey]);
            });
        }
        else{
            toReturn[key] = ob[key];
        }
    });

    return toReturn;
}

const restoreFloat = (obj) => {
    Object.keys(obj).forEach((key) => {
        const value = obj[key];
        if(_.isString(value)){
            obj[key] = parseFloat(value);
        }
        else{
            obj[key] = restoreFloat(value);
        }
    });
    return obj;
}


class ResultPage extends  Component{
    constructor(props) {
        super(props);
        this.state = {
            loading: true
        };
    }

    displayRows = (columns, vector) => {
        return Object.keys(vector).map((key) => 
            columns[key] ? <li key={key}><ScoreBar score={vector[key]} delay={3} label={columns[key]}/></li> : null
        );
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
            if(jsondata.error){
                return <ErrorPage message={jsondata.error_message}/>
            }
            else{
                const {columns, doc_id} = jsondata;
                const score = parseFloat(jsondata.score);
                const vector = restoreFloat(flattenObject(jsondata.result));
                return (
                    <div className='resultpage-container'>
                        <div className='reaultpage-indicator'>The Overall Similarity Score is: </div>
                        <div className='reaultpage-overall-container'><ScoreDisplay score={score} delay={3} /></div>
                        <div className='reaultpage-indicator'>Details: </div>
                        <ul className='resultpage-detaillist-container'>{this.displayRows(columns, vector)}</ul>
                        <div className='reaultpage-indicator'>We believe two accounts are {score >= 0.5 ? null : "not"} belonged to one user.</div>
                        <Feedback doc_id={doc_id} prediction={score >= 0.5 ? 1 : 0}/>
                    </div>
                );
            }
        }
    }
}

export default ResultPage;