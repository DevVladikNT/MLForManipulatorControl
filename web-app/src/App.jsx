import { useState } from 'react';
import { Card, Flex, Button, TextInput, Text, Title, Metric, Divider} from "@tremor/react";

import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';
import AnimationWindow from './fragments/AnimationWindow';
import Settings from './fragments/Settings';

function App() {
  const [animationData, setAnimationData] = useState({});

  return (
    <>
      <Flex
        flexDirection='row'
        alignItems='stretch'>
          <AnimationWindow
            animationData={animationData}/>
          <Settings
            setAnimationData={setAnimationData}/>
      </Flex>
    </>
  )
}

export default App
