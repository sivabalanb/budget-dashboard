import { ResponsiveBar } from '@nivo/bar'
import { useState, useEffect } from "react";
import { ResponsiveSwarmPlot } from '@nivo/swarmplot'


// make sure parent container have a defined height when using
// responsive component, otherwise height will be 0 and
// no chart will be rendered.
// website examples showcase many properties,
// you'll often use just a few of them.
export default function MyResponsiveBar(data){
    useEffect(() => {
        console.log("d", data.data)
        // console.log("barchart", data.data, typeof(data.data), typeof(data.data[0]['merchant']), typeof(data.data[0]['amount']))
        // console.log("d", d, typeof(d), typeof(d[0]['merchant']), typeof(d[0]['amount']))
    }, [data]);

    return (
    // <ResponsiveBar
    //     data={data.data}
    //     keys={[
    //         'amount',
    //     ]}
    //     indexBy="merchant"
    //     margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
    //     padding={0.3}
    //     layout="horizontal"
    //     // valueScale={{ type: 'linear' }}
    //     indexScale={{ type: 'band', round: true }}
    //     colors={{ scheme: 'nivo' }}       
        
    //     borderColor={{
    //         from: 'color',
    //         modifiers: [
    //             [
    //                 'darker',
    //                 1.6
    //             ]
    //         ]
    //     }}
    //     axisTop={null}
    //     axisRight={null}
    //     axisBottom={{
    //         tickSize: 5,
    //         tickPadding: 5,
    //         tickRotation: 0,
    //         legend: 'Merchant',
    //         legendPosition: 'middle',
    //         legendOffset: 32
    //     }}
    //     axisLeft={{
    //         tickSize: 5,
    //         tickPadding: 5,
    //         tickRotation: 0,
    //         legend: 'Amount',
    //         legendPosition: 'middle',
    //         legendOffset: -40
    //     }}
    //     labelSkipWidth={12}
    //     labelSkipHeight={12}
    //     labelTextColor={{
    //         from: 'color',
    //         modifiers: [
    //             [
    //                 'darker',
    //                 1.6
    //             ]
    //         ]
    //     }}
    //     legends={[
    //         {
    //             dataFrom: 'keys',
    //             anchor: 'bottom-right',
    //             direction: 'column',
    //             justify: false,
    //             translateX: 120,
    //             translateY: 0,
    //             itemsSpacing: 2,
    //             itemWidth: 100,
    //             itemHeight: 20,
    //             itemDirection: 'left-to-right',
    //             itemOpacity: 0.85,
    //             symbolSize: 20,
    //             effects: [
    //                 {
    //                     on: 'hover',
    //                     style: {
    //                         itemOpacity: 1
    //                     }
    //                 }
    //             ]
    //         }
    //     ]}
    //     role="application"
    //     // ariaLabel="Nivo bar chart demo"
    //     // barAriaLabel={function(e){return e.id+": "+e.formattedValue+" in merchant: "+e.indexValue}}
    // />

    <ResponsiveSwarmPlot
    data={data.data}
    groups={['category']}
    identity="merchant"
    value="amount"
    valueFormat="$.2f"
    valueScale={{ type: 'linear', min: 0, max: 1250, reverse: false }}
    size={{
        key: 'amount',
        values: [
            50,
            17
        ],
        sizes: [
            40,
            17
        ]
    }}
    forceStrength={4}
    simulationIterations={100}
    borderColor={{
        from: 'color',
        modifiers: [
            [
                'darker',
                0.6
            ],
            [
                'opacity',
                0.5
            ]
        ]
    }}
    margin={{ top: 80, right: 100, bottom: 80, left: 100 }}
    axisTop={{
        orient: 'top',
        tickSize: 10,
        tickPadding: 5,
        tickRotation: 0,
        legend: 'group if vertical, price if horizontal',
        legendPosition: 'middle',
        legendOffset: -46
    }}
    axisRight={{
        orient: 'right',
        tickSize: 10,
        tickPadding: 5,
        tickRotation: 0,
        legend: 'price if vertical, group if horizontal',
        legendPosition: 'middle',
        legendOffset: 76
    }}
    axisBottom={{
        orient: 'bottom',
        tickSize: 10,
        tickPadding: 5,
        tickRotation: 0,
        legend: 'group if vertical, price if horizontal',
        legendPosition: 'middle',
        legendOffset: 46
    }}
    axisLeft={{
        orient: 'left',
        tickSize: 10,
        tickPadding: 5,
        tickRotation: 0,
        legend: 'price if vertical, group if horizontal',
        legendPosition: 'middle',
        legendOffset: -76
    }}
/>
    )
    }

// export default MyResponsiveBar;