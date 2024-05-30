import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function EditProfile() {

    return (
      <>
        <h1>Edit Profile</h1>
        <Form>
            <Form.Group className="mb-3">
                <Form.Label>Display Name</Form.Label>
                <Form.Control type="text" placeholder="Enter a display name" />
            </Form.Group>

            <Form.Group className="mb-3" >
                <Form.Label>Politiacal Affiliations</Form.Label>
                <br/>
                <Form.Text muted>To select multiple affiliations hold down ctrl button.</Form.Text>
            </Form.Group>
   
            <Button variant="primary" type="submit">
                Submit
            </Button>
        </Form>
      </>
    )
  }
  
  export default EditProfile