import { useOutletContext } from "react-router-dom";
import EditProfile from "../components/EditProfile"

function ProfilePage() {
    const { user } = useOutletContext();

    return (
      <>
        <h1>Profile</h1>
        <EditProfile user={user}/>
      </>
    )
  }
  
  export default ProfilePage