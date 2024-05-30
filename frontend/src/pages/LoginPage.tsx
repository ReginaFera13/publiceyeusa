import { useState } from 'react'
import { useOutletContext, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { userLogin  } from '../utilities';

function LoginPage() {
    const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
    const { setUser } = useOutletContext();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        let response = await userLogin(email, password);
        setUser(response);
        navigate("/");
      };

    return (
      <>
        <h1>Signup</h1>
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email" onChange={(e) => setEmail(e.target.value)} />
                <Form.Text className="text-muted" >
                We'll never share your email with anyone else.
                </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicCheckbox">

            </Form.Group>
            <Button variant="primary" type="submit">
                Submit
            </Button>
        </Form>
      </>
    )
  }
  
  export default LoginPage