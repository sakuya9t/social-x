import React, {Component} from 'react';
import './index.css';
import { Dropdown, InputGroup, DropdownButton, FormControl } from 'react-bootstrap';

class QueryItem extends Component{
    constructor(props){
        super(props);
        this.state = {
            platformName: "Choose One.."
        };
    }

    selectMedia = (e) => {
        const platformName = e;
        this.setState(() => {
            return {platformName: platformName}
        });
    }

    render = () => {
        const {width} = this.props;
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
                <FormControl aria-describedby="basic-addon1" />
            </InputGroup>
        </div>
    }
}

export default QueryItem;