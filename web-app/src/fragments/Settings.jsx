import axios from "axios";
import { Card, Flex, Button, NumberInput, Text, Title, Metric, Divider, Select, SelectItem} from "@tremor/react";
import { useEffect, useState, useRef } from "react";

function Settings(props) {

    const [L1, setL1] = useState(5);
    const [L2, setL2] = useState(3);
    const [L3, setL3] = useState(2);
    const [W1, setW1] = useState(50);
    const [W2, setW2] = useState(30);
    const [W3, setW3] = useState(20);
    const [A1, setA1] = useState(0);
    const [A2, setA2] = useState(0);
    const [A3, setA3] = useState(0);
    const [G1, setG1] = useState(6);
    const [G2, setG2] = useState(4);
    const [M, setM] = useState(1);
    const [type, setType] = useState('nn');

    const [targetA1, setTargetA1] = useState(0);
    const [targetA2, setTargetA2] = useState(0);
    const [targetA3, setTargetA3] = useState(0);
    const [targetTime, setTargetTime] = useState(10);

    const get_animation = async () => {
        const data = {
            'lengths': [L1, L2, L3],
            'weights': [W1, W2, W3],
            'angles': [A1, A2, A3],
            'goal_point': [G1, G2],
            'additional_m': M,
            'target_angles': [targetA1, targetA2, targetA3],
            'target_time': targetTime,
        };
        const result = await axios.post(`http://localhost:2000/${type}`, data).catch((error) => {
        });
        props.setAnimationData(result.data);
    };

    return (
        <Card className="mr-4 mt-4 min-w-[300px] flex flex-col">
            <Text className="mb-2">Длины звеньев:</Text>
            <Flex className="gap-4">
                <NumberInput
                    placeholder="Amount"
                    min={0}
                    value={L1}
                    onValueChange={setL1}
                    disabled
                />
                <NumberInput
                    placeholder="Amount"
                    min={0}
                    value={L2}
                    onValueChange={setL2}
                    disabled
                />
                <NumberInput
                    placeholder="Amount"
                    min={0}
                    value={L3}
                    onValueChange={setL3}
                    disabled
                />
            </Flex>

            <Divider/>

            <Text className="mb-2">Массы звеньев:</Text>
            <Flex className="gap-4">
                <NumberInput
                    placeholder="Amount"
                    min={0}
                    value={W1}
                    onValueChange={setW1}
                    disabled
                />
                <NumberInput
                    placeholder="Amount"
                    min={0}
                    value={W2}
                    onValueChange={setW2}
                    disabled
                />
                <NumberInput
                    placeholder="Amount"
                    min={0}
                    value={W3}
                    onValueChange={setW3}
                    disabled
                />
            </Flex>

            <Divider/>

            <Text className="mb-2">Начальные углы:</Text>
            <Flex className="gap-4">
                <NumberInput
                    placeholder="Amount"
                    step={0.1}
                    value={A1}
                    onValueChange={setA1}
                />
                <NumberInput
                    placeholder="Amount"
                    step={0.1}
                    value={A2}
                    onValueChange={setA2}
                />
                <NumberInput
                    placeholder="Amount"
                    step={0.1}
                    value={A3}
                    onValueChange={setA3}
                />
            </Flex>

            <Divider/>

            <Flex className="gap-4">
                {type == 'simple' ?
                <>
                    <Flex flexDirection="col">
                        <Text className="self-start mb-2">Время выполнения:</Text>
                        <NumberInput
                            placeholder="Amount"
                            min={1}
                            value={targetTime}
                            onValueChange={setTargetTime}
                        />
                    </Flex>
                </>
                :
                <div>
                    <Text className="mb-2">Целевое положение:</Text>
                    <Flex className="gap-4">
                        <NumberInput
                            placeholder="Amount"
                            value={G1}
                            onValueChange={setG1}
                        />
                        <NumberInput
                            placeholder="Amount"
                            value={G2}
                            onValueChange={setG2}
                        />
                    </Flex>
                </div>
                }

                <div>
                    <Text className="mb-2">Масса груза:</Text>
                    <Flex className="gap-4">
                        <NumberInput
                            placeholder="Amount"
                            min={0}
                            value={M}
                            onValueChange={setM}
                        />
                    </Flex>
                </div>
            </Flex>

            {type == 'simple' ?
            <>
                <Divider/>
                <Text className="mb-2">Целевые углы:</Text>
                <Flex className="gap-4">
                    <NumberInput
                        placeholder="Amount"
                        step={0.1}
                        value={targetA1}
                        onValueChange={setTargetA1}
                    />
                    <NumberInput
                        placeholder="Amount"
                        step={0.1}
                        value={targetA2}
                        onValueChange={setTargetA2}
                    />
                    <NumberInput
                        placeholder="Amount"
                        step={0.1}
                        value={targetA3}
                        onValueChange={setTargetA3}
                    />
                </Flex>
            </> : <></>}
            
            <Divider/>

            <Flex className="gap-4">
                <Select
                    value={type}
                    onValueChange={setType}>
                    <SelectItem value="simple">Релейный алгоритм</SelectItem>
                    <SelectItem value="greedy">Жадный алгоритм</SelectItem>
                    <SelectItem value="nn">Нейросетевой алгоритм</SelectItem>
                </Select>
                <Button
                    className="self-start"
                    onClick={get_animation}
                >Выполнить</Button>
            </Flex>

        </Card> 
    );

}

export default Settings;