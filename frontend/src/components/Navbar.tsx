import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

function MyNavbar() {
  return (
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="#home">
            <img
              alt=""
              src="logo.png"
              width="30"
              height="30"
              className="d-inline-block align-top"
            />{' '}
            PublicEyeUSA
        </Navbar.Brand>
        <Navbar.Text>Welcome, Mark Otto!</Navbar.Text>{' '}
          <Nav className="me-auto">
            <NavDropdown title="Menu" id="basic-nav-dropdown">
              <NavDropdown.Item href="#home">Home</NavDropdown.Item>
              <NavDropdown.Item href="#signup">Signup</NavDropdown.Item>
              <NavDropdown.Item href="#login">Login</NavDropdown.Item>
            </NavDropdown>
          </Nav>
      </Container>
    </Navbar>
  );
}

export default MyNavbar;