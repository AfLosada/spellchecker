import logo from './logo.svg';
import './App.css';
import Form from './components/Form.js'
import Lista from './components/List.js'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          <h1>Ingrese la frase para ser corregida</h1>
          <Form/>
        </p>
        <Lista/>

      </header>
    </div>
  );
}

export default App;
