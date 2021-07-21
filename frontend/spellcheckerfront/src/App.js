import logo from './logo.svg';
import './App.css';
import Form from './components/Form.js'
import Lista from './components/List.js'

function App() {
  return (
    <div className="App">
          <div className="col">
            <header className="App-header">
              <p>
                <h1>Ingrese la frase que será corregida</h1>
                <br></br>
                <Form />
              </p>
            </header>
          </div>
          <div className="row">
            <div className="col">
                <Lista />
            </div>
          </div>
    </div>
  );
}

export default App;
