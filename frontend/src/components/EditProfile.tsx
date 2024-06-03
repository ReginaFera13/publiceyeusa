import { useEffect, useState } from "react";
import { useOutletContext } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { getUserProfile, putUserProfile, getAffilations } from "../utilities";

function EditProfile({ setToggleEdit }) {
    const { user, userProfileData, setUserProfileData } = useOutletContext();
    const [affiliations, setAffiliations] = useState([]);
    const [userAffiliations, setUserAffiliations] = useState([]);
    const [userAffiliationIDs, setUserAffiliationIDs] = useState([]);
    const [displayName, setDisplayName] = useState([]);

    const fetchAffiliations = async () => {
        const affiliations = await getAffilations();
        setAffiliations(affiliations);
    };

    const userProfile = async () => {
        const profileData = await getUserProfile(user);
        setDisplayName(profileData.display_name);
        setUserAffiliations(profileData.affiliations.map((aff) => aff.category));
    };

    const updateUserProfile = async () => {
        const upload_data = {
            affiliations: userAffiliationIDs,
            display_name: displayName,
        };
        const responseStatus = await putUserProfile(upload_data);
        if (responseStatus) {
            setUserProfileData(responseStatus);
        }
    };

    function handleSubmit(e) {
        e.preventDefault();
        updateUserProfile();
        setToggleEdit(false)
    }

    useEffect(() => {
        userProfile();
        fetchAffiliations();
    }, []);

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
                    {affiliations.map((affilaition, index) => (
                      <option key={index} data-key={affilaition.id} value={affilaition.category}>
                        {affilaition.category}
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
  
  export default EditProfile