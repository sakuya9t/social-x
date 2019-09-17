import React, {Component} from 'react';
import { faCheckCircle, faMinusCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import './index.css';

class LoginValidation extends Component{
    render = () => {
        const {valid} = this.props;
        if(valid === null) return null;
        if(valid){
            return <p className='validation-success'>
                        <FontAwesomeIcon icon={faCheckCircle} />
                         &nbsp;Verification successful
                    </p>
        }
        else{
            return <p className='validation-failed'>
                        <FontAwesomeIcon icon={faMinusCircle} />
                        &nbsp;Verification failed
                    </p>
        }
    }
}

export default LoginValidation;