import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';

function SignupBttn() {

  return (
  <>
    <Button variant="primary" as={Link} to="/signup">Signup</Button>
  </>
  )
}
  
export default SignupBttn