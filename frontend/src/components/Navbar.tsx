import { useEffect } from 'react';
import { Link, useNavigate } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { logoutUser } from '../store/authSlice';

function MyNavbar() {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { user, loading } = useAppSelector((state) => state.auth);
  const { profile } = useAppSelector((state) => state.profile);

  const handleUserLogout = async () => {
    dispatch(logoutUser())
      .then(() => {
        navigate("/");
      })
      .catch((error) => {
        console.error('Logout failed:', error);
      });
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
      {user && profile && ( // Render welcome message and  logout link only if user is logged in
        <>
          <Navbar.Text>Welcome, {profile.display_name}</Navbar.Text>
          <Nav.Link onClick={handleUserLogout} disabled={loading}>
            {loading ? 'Logging out...' : 'Logout'}
          </Nav.Link>
        </>
      )}
    </Container>
  </Navbar>
  );
}

export default MyNavbar;