import React from "react"
export class Form extends React.Component {

    constructor(props) {
        super(props);
        this.state = { "text": '' };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange = (event) => {
        this.setState({["text"]: event.target.value});
      }

    handleSubmit(event) {
        this.sendRequest();
        //event.preventDefault();
        alert("Se está arreglando la ortografía de la oración")
    }

    sendRequest() {
        console.log("Entrando al fetch")
        fetch('http://localhost:3000/dev/spellcheck', {
            method: 'POST',
            // We convert the React state to JSON and send it as the POST body
            body: JSON.stringify(this.state)
        }).then(function (response) {
            console.log(response)
            return response.json();
        });
    }

    render() {
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <input type="text" value={this.state.value} onChange={this.handleChange} />
                    <input type="submit" value="Ingresar"/>
                </form>
            </div>
        );
    }
}

export default Form;