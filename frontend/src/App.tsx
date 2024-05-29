import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import HomePage from "./pages/HomePage";
import MyNavbar from './components/Navbar';

function App() {

  return (
  <>
    <MyNavbar/>
    <HomePage/>
  </>
  )
}

export default App
