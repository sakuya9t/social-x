import React, {Component} from 'react';
import './index.css';
import { BounceLoader } from 'react-spinners';

class ResultPage extends  Component{
    constructor(props) {
        super(props);
        this.state = {
            loading: true
        };
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
            return (
                <div className='resultpage-container'>
                    {data}
                </div>
            );
        }
    }
}

export default ResultPage;