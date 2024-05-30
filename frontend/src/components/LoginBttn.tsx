import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';

function LoginBttn() {

    return (
      <>
        <Button variant="primary" as={Link} to="/login">Login</Button>
      </>
    )
  }
  
  export default LoginBttn