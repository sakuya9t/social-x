import React, {Component} from 'react';
import './index.css';
import Image from '../../resources/refresh-512.png';

class ResetButton extends Component{
    render = () => <div className='resetbtn-container' onClick={() => window.location.reload()}>
        <img src={Image} alt='reset' width={70} height={70}/>
    </div>
}
export default ResetButton;