import { useEffect } from 'react';
import { Outlet, useNavigate, useLocation } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import MyNavbar from './components/Navbar';
import { useAppDispatch, useAppSelector } from './store/hooks';
import { confirmUser } from './store/authSlice';
import { fetchProfile } from './store/profileSlice';
import { fetchAffiliations } from './store/affiliationsSlice';

function App() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const { user, loading } = useAppSelector((state) => state.auth);

  useEffect(() => {
    if (!user) {
      dispatch(confirmUser());
      dispatch(fetchProfile());
      dispatch(fetchAffiliations())
    }
  }, [dispatch, user]);

  useEffect(() => {
    const allowNonUserUrls = ["/login", "/signup", "/"]; // should allow if not logged in
    const homePage = '/';

    const isAllowedNonUserUrl = allowNonUserUrls.includes(location.pathname);

    if (user && location.pathname === '/') {
      navigate("/profile");
    } else if (!user && !isAllowedNonUserUrl) {
      navigate("/");
    }
  }, [user, location.pathname, navigate]);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <>
      <MyNavbar/> 
      <Outlet/> 
    </>
  );
}

export default App;
