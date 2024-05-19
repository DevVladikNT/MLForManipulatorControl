import { useState } from 'react';
import { Card, Flex, Button, TextInput, Text, Title, Metric, Divider} from "@tremor/react";

import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';
import AnimationWindow from './fragments/AnimationWindow';
import Settings from './fragments/Settings';

function App() {
  const [type, setType] = useState('nn');
  const [animationData, setAnimationData] = useState({});
  const [needHelp, setNeedHelp] = useState(false);

  return (
    <>
      <Flex
        flexDirection='row'
        alignItems='start'>
          <AnimationWindow
            type={type}
            animationData={animationData}
            needHelp={needHelp}/>
          
          <Settings
            type={type}
            setType={setType}
            setAnimationData={setAnimationData}
            needHelp={needHelp}
            setNeedHelp={setNeedHelp}/>
      </Flex>
    </>
  )
}

export default App
