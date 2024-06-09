import Button from 'react-bootstrap/Button';
import { useAppSelector } from '../store/hooks';

function ProfileInfo({ setToggleEdit }) {
  const { profile } = useAppSelector((state) => state.profile);

  const handleEditClick = () => {
    setToggleEdit(true);
  };

  return (
    <>
      {profile && ( // Check if profile exists
        <>
          <h3>{profile.display_name}</h3>
          {profile.affiliations && profile.affiliations.map((aff, i) => (
            <li key={i}>{aff.category}</li>
          ))}
          <Button onClick={handleEditClick}>Edit Profile</Button>
        </>
      )}
    </>
  )
}
  
export default ProfileInfo