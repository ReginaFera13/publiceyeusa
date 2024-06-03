import { Link, useNavigate } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { userLogout } from "../utilities";

function MyNavbar({ userProfileData, setUserProfileData, user, setUser }) {
  const navigate = useNavigate();

  const handleUserLogout = async () => {
		const loggedOut = await userLogout();
		if (loggedOut) {
			setUser(null);
			setUserProfileData([]);
			navigate("/")
		}
	};

  return (
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand as={Link} to="/">
            <img
              alt=""
              src="logo.png"
              width="30"
              height="30"
              className="d-inline-block align-top"
            />{' '}
            PublicEyeUSA
        </Navbar.Brand>
        {userProfileData && (
          <>
            <Navbar.Text>Welcome, {userProfileData.display_name}</Navbar.Text>
            {/* <Nav.Link onClick={handleUserLogout}>Logout</Nav.Link> */}
          </>
        )}
        <Nav.Link onClick={handleUserLogout}>Logout</Nav.Link>
      </Container>
    </Navbar>
  );
}

export default MyNavbar;