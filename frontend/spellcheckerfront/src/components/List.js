import React from "react";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';

export default class Lista extends React.Component {

    constructor(props) {
        super(props);
        this.state = { petitions: [], responses: [] };
    }

    componentDidMount() {
        fetch("http://localhost:3000/dev/spellcheck", { method: "GET" })
            .then(res => {
                return res.json()
            })
            .then(
                (result) => {
                    let row = []
                    let petitions = result["petitions"]
                    for (let i = 0; i < petitions.length; i++) {
                        let row = petitions[i]
                        this.setState({
                            petitions: this.state.petitions.concat(row[0]),
                            responses: this.state.responses.concat(row[1])
                        })
                    }
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )
    }

    render() {
        const { petitions, responses } = this.state;
        return (
            <div className="containderfluid">
                <div className="row justify-content-center">
                    <div className="col-4">
                        <p className="demo">Peticiones</p>
                        <ul className="demo">
                            {petitions.map((item, index) => {
                                return <li className="demo" key={index}><button className="button">{item}</button></li>
                            })}
                        </ul>
                    </div>
                    <div className="col-2"></div>
                    <div className="col-4">
                        <p className="demo">Respuestas</p>
                        <ul className="demo">
                            {responses.map((item, index) => {
                                return <li className="demo" key={index}><button className="button">{item}</button></li>
                            })}
                        </ul>
                    </div>
                </div>
            </div>

        );
    }
}
