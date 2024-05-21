import { useState } from 'react';
import { Flex } from "@tremor/react";

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
