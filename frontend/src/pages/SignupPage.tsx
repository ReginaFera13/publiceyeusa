import { useEffect, useState } from 'react'
import { useOutletContext, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { userRegistration } from '../utilities';

function SignupPage() {
    const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
    const { setUser } = useOutletContext();
    const navigate = useNavigate();

    const handleSignUp = async(e) => {
		e.preventDefault();
        const userData = await userRegistration(email, password);
		setUser(userData);
		navigate("/")
    }

    return (
      <>
        <h1>Signup</h1>
        <Form onSubmit={handleSignUp}>
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
            <Form.Check 
                type="checkbox" 
                label={
                    <>
                    I have read and agree to PublicEyeUSA's <Link to='/terms'>Terms of Service</Link> and <Link to='/privacy'>Privacy Policy</Link>
                    </>
                }
            />
            </Form.Group>
            <Button variant="primary" type="submit">
                Submit
            </Button>
        </Form>
      </>
    )
  }
  
  export default SignupPage