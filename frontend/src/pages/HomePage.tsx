import SignupBttn from "../components/SignupBttn"
import LoginBttn from "../components/LoginBttn"

function HomePage() {

    return (
      <>
        <h1>PublicEyeUSA</h1>
        <h3>Making Politics Transparent</h3>
        <SignupBttn/>{' '}
        <LoginBttn/>
      </>
    )
  }
  
  export default HomePage