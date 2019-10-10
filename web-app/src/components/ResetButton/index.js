import React, {Component} from 'react';
import './index.css';
import Image from '../../resources/refresh-512.png';

class ResetButton extends Component{
    render = () => <div className='resetbtn-container' onClick={() => window.location.reload()}>
        <img src={Image} alt='reset' width={80} height={80}/>
    </div>
}
export default ResetButton;