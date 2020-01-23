import React from 'react';
import Form from "react-bootstrap/Form";
import {Button} from "react-bootstrap";

export class Search extends React.Component {
    constructor(props) {
    super(props);
    this.state = {value: ''};
    //this.handleChange = this.handleChange.bind(this);
    //this.handleSubmit = this.handleSubmit.bind(this);
  }

  render() {
    return (
        <Form>
          <Form.Group>
            <Form.Label>Search</Form.Label>
            <Form.Control type="text" placeholder="" />
          </Form.Group>
          <Button variant="primary">Submit</Button>
        </Form>
    );
  }
}
