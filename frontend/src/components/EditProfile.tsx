import { useEffect, useState } from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { updateProfile } from '../store/profileSlice'; // Import the updateUserProfile action
import { useAppDispatch, useAppSelector } from '../store/hooks';

function EditProfile({ setToggleEdit }) {
  const dispatch = useAppDispatch();
  const [userAffiliations, setUserAffiliations] = useState([]);
  const [userAffiliationIDs, setUserAffiliationIDs] = useState([]);
  const [displayName, setDisplayName] = useState('');
  const { profile } = useAppSelector((state) => state.profile);
  const { affiliations } = useAppSelector((state) => state.affiliations);

  const updateUserProfileData = () => {
    const uploadData = {
      affiliations: userAffiliationIDs,
      display_name: displayName,
    };
    dispatch(updateProfile(uploadData)); // Dispatch the updateUserProfile action with the updated data
  };

  function handleSubmit(e) {
    e.preventDefault();
    updateUserProfileData();
    setToggleEdit(false);
  }

  useEffect(() => {
    if (profile) {
      setDisplayName(profile.display_name || ''); // Set display name if available
      setUserAffiliations(profile.affiliations.map((aff) => aff.category));
      setUserAffiliationIDs(profile.affiliations.map((aff) => aff.id));
    }
  }, [profile]);

  return (
  <>
    <h3>Edit Profile</h3>
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="display_name">
        <Form.Label>Display Name</Form.Label>
        <Form.Control type="text" placeholder="Enter a display name" value={displayName} onChange={e => setDisplayName(e.target.value)} />
      </Form.Group>

      <Form.Group className="mb-3" controlId="affiliations">
        <Form.Label>Political Affiliations</Form.Label>
        <br/>
        <Form.Text muted>To select multiple affiliations hold down ctrl button.</Form.Text>
        <Form.Control 
          as="select" 
          multiple value={userAffiliations} 
          onChange={(e) => {
            const selectedOptions = Array.from(e.target.selectedOptions);
            const values = selectedOptions.map(option => option.value);
            const ids = selectedOptions.map(option => parseInt(option.getAttribute('data-key')));

            setUserAffiliations(values);
            setUserAffiliationIDs(ids);
          }}>
          {affiliations.map((affiliation, index) => (
            <option key={index} data-key={affiliation.id} value={affiliation.category}>
              {affiliation.category}
            </option>
          ))}
        </Form.Control>
      </Form.Group>
  
      <Button variant="primary" type="submit">
        Submit
      </Button>
    </Form>
  </>
  )
}

export default EditProfile;