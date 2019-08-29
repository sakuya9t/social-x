import React, {Component} from 'react';
import './index.css';
import { Dropdown, InputGroup, DropdownButton, FormControl } from 'react-bootstrap';

class QueryItem extends Component{
    constructor(props){
        super(props);
        this.state = {
            platformName: "Choose One..",
            loginChecked: false,
            text: ""
        };
    }
    
    selectMedia = (e) => {
        const setData = this.props.setData;
        const platformName = e;
        setData({
            ...this.state,
            platformName: platformName
        });
        this.setState({
            ...this.state,
            platformName: platformName
        });
    }

    onLoginChecked = (e) => {
        const setData = this.props.setData;
        const checked = e.target.checked;
        setData({
            ...this.state,
            loginChecked: checked
        });
        this.setState({
            ...this.state,
            loginChecked: checked
        });
    }

    onTextChanged = (e) => {
        const setData = this.props.setData;
        const text = e.target.value;
        setData({
            ...this.state,
            text: text
        });
        this.setState({
            ...this.state,
            text: text
        });
    }

    render = () => {
        const {width, itemkey} = this.props;
        const {platformName} = this.state;
        return <div className="queryitem-container" style={{width: width}}>
            <InputGroup className="mb-3">
                <DropdownButton
                    as={InputGroup.Prepend}
                    onSelect={this.selectMedia}
                    variant="outline-secondary"
                    title={<span className="queryitem-dropdown-fixwidth">{platformName}</span>}
                    id="input-group-dropdown-1"
                >
                <Dropdown.Item eventKey="Instagram">Instagram</Dropdown.Item>
                <Dropdown.Item eventKey="Twitter">Twitter</Dropdown.Item>
                <Dropdown.Item eventKey="Foursquare">Foursquare</Dropdown.Item>
                <Dropdown.Item eventKey="Flickr">Flickr</Dropdown.Item>
                </DropdownButton>
                <FormControl aria-describedby="basic-addon1" onChange={this.onTextChanged} />
            </InputGroup>
            <p>
                <input
                    name="login"
                    id={`login${itemkey}`}
                    type="checkbox"
                    checked={this.state.isGoing}
                    onChange={this.onLoginChecked} />
                
                <label className="queryitem-label" htmlFor={`login${itemkey}`}>Login your account </label>
            </p>
        </div>
    }
}

export default QueryItem;