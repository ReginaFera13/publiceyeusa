import { useEffect, useState } from "react";
import { useOutletContext } from "react-router-dom";
import Button from 'react-bootstrap/Button';

function ProfileInfo({ setToggleEdit }) {
    const { userProfileData } = useOutletContext();

    const handleEditClick = () => {
        setToggleEdit(true);
      };

    return (
      <>
        <h3>{userProfileData.display_name}</h3>
        {userProfileData.affiliations && userProfileData.affiliations.map((aff, i) => (
            <li key={i}>{aff.category}</li>
        ))}
        <Button onClick={handleEditClick}>Edit Profile</Button>
      </>
    )
  }
  
  export default ProfileInfo