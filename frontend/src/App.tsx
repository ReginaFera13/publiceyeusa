import { useEffect, useState } from 'react'
import { Outlet, useNavigate, useLocation, useLoaderData } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import MyNavbar from './components/Navbar';

function App() {
  const initialUser = useLoaderData();
  const [user, setUser] = useState(initialUser);
  // const [userProfileData, setUserProfileData] = useState([])
  const navigate = useNavigate();
  const location = useLocation();

  console.log('USER', user)

  useEffect(() => {
    // const fetchUserProfile = async () => {
    //   if (user) {
    //     try {
    //       const userProfileData = await getUserProfile(user);
    //       setUserProfileData(userProfileData);
    //       // console.log('User profile data loaded:', userProfileData);
    //     } catch (error) {
    //       console.error('Error fetching user profile data:', error);
    //     }
    //   }
    // };
  
    // fetchUserProfile();
  
    let nullUserUrls = ["/login", "/signup"] // should redirect to profile if logged in
    let allowNonUserUrls = ["/login", "/signup", "/"] // should allow if not logged in
  
      // check if current url is one that might need to redirect
      let isNullUserUrl = nullUserUrls.includes(location.pathname)
      let isAllowedNonUserUrl = allowNonUserUrls.includes(location.pathname);
  
  
      // redirect to profile page when
      // logged user tries to go to signup, etc
      if(user && isNullUserUrl) {
        navigate("/")
      }
  
      // not logged in user tries to go anywhere BUT signup, login, home or events
      // we redirect because the user needs to log in before they do anything else
      else if (!user && !isAllowedNonUserUrl){
        navigate("/")
      }
  
    }, [user, location.pathname]);

  return (
  <>
    <MyNavbar user={ user } setUser={ setUser }/>
    <Outlet context={{ user, setUser }}/>
  </>
  )
}

export default App
