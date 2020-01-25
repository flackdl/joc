import React from 'react';
import spinner from '../spinner.gif';

export class Search extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            query: '',
            isLoading: false,
            results: null,
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({query: event.target.value});
    }

    handleSubmit(event) {
        this.setState({isLoading: true});
        fetch(`https://joy-of-cooking.herokuapp.com/api/recipe/?search=${this.state.query}`).then((result) => {
            result.json().then((data) => {
                this.setState({results: data.results, isLoading: false});
            })
        });
        event.preventDefault();
    }

    results() {
        if (this.state.results) {
            if (this.state.results.length > 0) {
                const results = this.state.results.map((result) => {
                    return <li key={result.id}>{result.name}</li>
                });
                return (
                    <ul>
                        {results}
                    </ul>
                );
            } else {
                return (
                    <p className={'alert alert-info'}>No results</p>
                )
            }
        }
    }

    spinner() {
        if (this.state.isLoading) {
            return (
                <img src={spinner} />
            )
        }
    }

    render() {
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <div className={'form-group'}>
                        <input type="text" className="form-control" value={this.state.query} placeholder={this.props.placeholder} onChange={this.handleChange}/>
                    </div>
                </form>
                {this.spinner()}
                {this.results()}
            </div>
        );
    }
}
