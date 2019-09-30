import React, {Component} from 'react';
import ScoreDisplay from '../ScoreDisplay';
import ScoreBar from '../ScoreBar';

class AboutPage extends Component{
    render = () => {
        return <>
            <ScoreDisplay score={0.2} delay={3} />
            <ScoreBar score={0.4825} delay={3} label={'abcdf'}/>
            <ScoreBar score={0.7794} delay={3} label={'def'}/>
        </>
    }
}
export default AboutPage;