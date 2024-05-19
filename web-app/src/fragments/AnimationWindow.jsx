import axios from "axios";
import { Card, Flex, Button, TextInput, Text, Title, Metric, Divider, LineChart} from "@tremor/react";
import { useEffect, useState, useRef } from "react";

function AnimationWindow(props) {

    const percentSize = 1000;
    const [accelArr, setAccelArr] = useState([]);

    const canvasRef = useRef(null);
    const draw = (ctx, frameCount, coordArr, goal) => {
        if (coordArr && Math.floor(frameCount/10) < coordArr.length) {
            ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
            ctx.fillStyle = 'white';
            ctx.strokeStyle = 'white';

            ctx.beginPath();
            ctx.arc(percentSize/2 + goal[0]*percentSize/2, percentSize/2 - goal[1]*percentSize/2, 15 * Math.sin(frameCount * 0.05) ** 2, 0, 2 * Math.PI);
            ctx.fill();
            ctx.closePath();

            ctx.beginPath();
            ctx.lineWidth = 1;
            ctx.moveTo(0, percentSize/2);
            ctx.lineTo(percentSize, percentSize/2);
            ctx.stroke();
            ctx.moveTo(percentSize/2, 0);
            ctx.lineTo(percentSize/2, percentSize);
            ctx.stroke();
            ctx.closePath();

            ctx.beginPath();
            ctx.moveTo(percentSize/2, percentSize/2);
            const first = [
                coordArr[Math.floor(frameCount/10)][0][0]*percentSize/2,
                coordArr[Math.floor(frameCount/10)][0][1]*percentSize/2
            ];
            const second = [
                first[0] + coordArr[Math.floor(frameCount/10)][1][0]*percentSize/2,
                first[1] + coordArr[Math.floor(frameCount/10)][1][1]*percentSize/2
            ];
            const third = [
                second[0] + coordArr[Math.floor(frameCount/10)][2][0]*percentSize/2,
                second[1] + coordArr[Math.floor(frameCount/10)][2][1]*percentSize/2
            ]
            ctx.lineTo(percentSize/2 + first[0], percentSize/2 - first[1]);
            ctx.lineTo(percentSize/2 + second[0], percentSize/2 - second[1]);
            ctx.lineTo(percentSize/2 + third[0], percentSize/2 - third[1]);
            ctx.lineWidth = percentSize/50;
            ctx.stroke();
            ctx.closePath();
        }
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        const ratio = window.devicePixelRatio || 1;
        context.scale(ratio, ratio);
      }, []);

    useEffect(() => {
        setAccelArr(props.animationData.accel);
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        const coordArr = props.animationData.coord;
        const goal = props.animationData.goal;

        let frameCount = 0;
        let animationFrameId;
        const render = () => {
          frameCount++;
          draw(context, frameCount, coordArr, goal);
          animationFrameId = window.requestAnimationFrame(render);
        };
        render();
        return () => {
          window.cancelAnimationFrame(animationFrameId);
        };
      }, [props]);

    return (
        <Card className="mr-4 mt-4 min-w-[300px] flex flex-col gap-4">
            <canvas
                width={`${(window.devicePixelRatio || 1) * percentSize}%`}
                height={`${(window.devicePixelRatio || 1) * percentSize}%`}
                className="w-full aspect-square"
                ref={canvasRef}
            />
            <LineChart 
                className="max-h-[200px]"
                index="step"
                categories={['Звено 1', 'Звено 2', 'Звено 3']}
                data={accelArr}
                showAnimation
            />
        </Card> 
    );

}

export default AnimationWindow;