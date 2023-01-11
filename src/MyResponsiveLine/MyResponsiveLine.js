import { useState, useEffect } from "react";
import { ResponsiveLine } from '@nivo/line';

const commonProperties = {
    // width: 900,
    // height: 400,
    // margin: { top: 20, right: 20, bottom: 60, left: 80 },
    margin:{ top: 80, right: 110, bottom: 10, left: 60 },
    animate: true,
    enableSlices: 'x',
}

export default function MyResponsiveLine(data){
    useEffect(() => {
        console.log("d", data.data)
        // console.log("barchart", data.data, typeof(data.data), typeof(data.data[0]['merchant']), typeof(data.data[0]['amount']))
        // console.log("d", d, typeof(d), typeof(d[0]['merchant']), typeof(d[0]['amount']))
    }, [data]);

    return (
<ResponsiveLine
        {...commonProperties}
        data={data.data}
        xScale={{
            type: 'time',
            format: '%Y-%m',
            useUTC: false,
            precision: 'month',
        }}
        xFormat="time:%Y-%m"
        yScale={{
            type: 'linear',
            // stacked: boolean('stacked', false),
        }}
        // axisLeft={{
        //     legend: 'linear scale',
        //     legendOffset: 12,
        // }}
        axisBottom={{
            format: '%b %y',
            tickValues: 'every 30 days',
            // legend: 'time scale',
            legendOffset: -12,
        }}
        // curve={select('curve', curveOptions, 'monotoneX')}
        enablePointLabel={true}
        // pointSymbol={CustomSymbol}
        pointSize={16}
        pointBorderWidth={1}
        pointBorderColor={{
            from: 'color',
            modifiers: [['darker', 0.3]],
        }}
        useMesh={true}
        enableSlices={false}
        legends={[
            {
                anchor: 'top',
                direction: 'row',
                justify: false,
                translateX: 10,
                translateY: -40,
                itemsSpacing: 0,
                itemDirection: 'left-to-right',
                itemWidth: 80,
                itemHeight: 20,
                itemOpacity: 0.75,
                symbolSize: 12,
                symbolShape: 'circle',
                symbolBorderColor: 'rgba(0, 0, 0, .5)',
                effects: [
                    {
                        on: 'hover',
                        style: {
                            itemBackground: 'rgba(0, 0, 0, .03)',
                            itemOpacity: 1
                        }
                    }
                ]
            }
        ]}
    />
    )
}