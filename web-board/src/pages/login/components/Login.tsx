import { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import { useUser } from '../../../context/UserContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { loginRequest } from '../../../utils/api';
import { ILogged } from '../../../utils/interfaces';
import './Login.css';


const Login =  () => {
  const { setUserNameId, setLoggedIn } = useUser();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loginInfo, setLoginInfo] = useState<ILogged>();
  const [IncorrectLogin, setIncorrectLogin] = useState(false);


  const handleLogin = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    loginRequest(username, password)
        .then((response) => {
          setLoginInfo(response);
          if (response?.success){
            if (response.credencialsTrobades && response.idUsuari != null){
              window.sessionStorage.setItem('username', response.idUsuari.toString())
              setUserNameId(response.idUsuari.toString());
              setLoggedIn(!!response.idUsuari);
              setIncorrectLogin(false);
            } else {
              setIncorrectLogin(true)
            }
          }
        })
        .catch((error) => {
          console.error('Error login): ', error);
        });
  };

  const handleRegister = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); //Nomes si no cal tornar a pagina login
    // TO-DO: agafar usuari i password i enviar peticio POST register
    // TO-DO: rebre resposta peticio
    // TO-DO: login?
  }

  const [expanded, setExpanded] = useState(true);

    return (
      <>
      {expanded &&(
        <div className="form-container login-container">
            <Form className="custom-form" onSubmit={handleLogin}>
            <h2>Inicia sessió</h2>
            {IncorrectLogin && <span className='incorrect-message'>Correu electrònic o contrassenya incorrectes. Torna a provar</span>}
            <Form.Group controlId="formBasicUsername">
              <Form.Label className="custom-label"><FontAwesomeIcon icon="user-large" style={{ color: "#007ABF" }} /> Nom d'usuari </Form.Label>
              <Form.Control className="custom-input" type="text" placeholder="Nom d'usuari" value={username} onChange={(e) => setUsername(e.target.value)} />
            </Form.Group>

            <Form.Group controlId="formBasicPassword">
              <Form.Label className="custom-label"><FontAwesomeIcon icon="key" style={{ color: "#007ABF" }} /> Contrasenya </Form.Label>
              <Form.Control className="custom-input" type="password" placeholder="Contrasenya" value={password} onChange={(e) => setPassword(e.target.value)} />
            </Form.Group>

            <Button className="form-button" variant="primary" type="submit">
              Iniciar Sessió <FontAwesomeIcon icon="right-to-bracket" style={{ color: "#FFFFFF" }} />
            </Button>
            <div className="login-register" onClick={() => setExpanded(prevState => !prevState) }><span>Registra un nou compte</span></div>
          </Form>
        </div>
      )}
      {!expanded &&(
        <div className="form-container login-container">
            <Form className="custom-form" onSubmit={handleRegister}>
            <h1>Registra un nou usuari</h1>
            <Form.Group controlId="formBasicUsername">
              <Form.Label className="custom-label"> <FontAwesomeIcon icon="user-large" style={{ color: "#007ABF" }} /> Nom d'usuari </Form.Label>
              <Form.Control className="custom-input" type="text" placeholder="Nom d'usuari" />
            </Form.Group>

            <Form.Group controlId="formBasicPassword">
              <Form.Label className="custom-label"><FontAwesomeIcon icon="key" style={{ color: "#007ABF" }} /> Nova Contrassenya </Form.Label>
              <Form.Control className="custom-input" type="password" placeholder="Contrassenya" />
            </Form.Group>

            <Button className="form-button" variant="primary" type="submit">
              Registra't <FontAwesomeIcon size='sm' icon="user-plus" style={{ color: "#FFFFFF" }} />
            </Button>
            <div className="login-register" onClick={() => setExpanded(prevState => !prevState) }><span>Inicia sessió d'un compte ja existent</span></div>
          </Form>
        </div>
      )}
      </>
    )
}

export default Login;