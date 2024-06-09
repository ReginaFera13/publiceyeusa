import { useState } from "react";
import ProfileInfo from "../components/ProfileInfo";
import EditProfile from "../components/EditProfile";

function ProfilePage() {
  const [toggleEdit, setToggleEdit] = useState(false)

  return (
    <>
      <h1>Profile</h1>
      {!toggleEdit ? 
        <ProfileInfo setToggleEdit={setToggleEdit}/>:
        null
      }
      {toggleEdit ? 
        <EditProfile setToggleEdit={setToggleEdit}/>:
        null
      }
      
    </>
  )
}

export default ProfilePage