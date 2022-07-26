import * as React from 'react'
import Home from './Home/Home';
import "./App.scss";

// 1. import `ChakraProvider` component
import { ChakraProvider } from '@chakra-ui/react'
import Header from "./Header/Header";

function App() {
  // 2. Wrap ChakraProvider at the root of your app
  return (
    <ChakraProvider>
      <Header />
      <Home />
    </ChakraProvider>
  )
}

export default App;