import { useState, useEffect } from "react";
import {
    Box,
    useColorMode,
    Heading,
    Text,
} from '@chakra-ui/react';
import { MoonIcon, SunIcon } from '@chakra-ui/icons';
import { Grid, GridItem } from '@chakra-ui/react'
import { Stack, HStack, VStack } from '@chakra-ui/react'
import { Select } from '@chakra-ui/react';
import { Flex, Spacer } from '@chakra-ui/react';
import { Button, ButtonGroup } from '@chakra-ui/react';
import { SimpleGrid } from '@chakra-ui/react'
import MyResponsivePie from '../MyResponsivePie/MyResponsivePie';

export default function Home() {
    const { colorMode, toggleColorMode } = useColorMode();
    const [month, setMonth] = useState([]);
    const [category, setCategory] = useState([]);
    const [pieChartDataMerchant, setPieChartDataMerchant] = useState([]);
    const [pieChartDataCategory, setPieChartDataCategory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    useEffect(() => {
        fetch(`http://127.0.0.1:5000/home`)
            .then((response) => response.json())
            // .then((actualData) => setMonth(actualData[0]['month']))
            .then((actualData) => {
                setMonth(actualData[0]['month'])
                setCategory(actualData[0]['category'])
                setPieChartDataMerchant(actualData[0]['pie_chart_data_merchant'])
                setPieChartDataCategory(actualData[0]['pie_chart_data_category'])
                setError(null);
                console.log("month", month)
                console.log("category", category)
                console.log("pie_chart_data_merchant", actualData[0]['pie_chart_data_merchant'])
                console.log("pie_chart_data_category", actualData[0]['pie_chart_data_category'])
                setLoading(false)
            })
            .catch((err) => {
                console.log(err.message);
            });
    }, [loading]);


    return (
        <>
            <Box bgGradient='linear(to-r, teal.500, green.500)'
                _hover={{
                    bgGradient: 'linear(to-r, red.500, yellow.500)',
                }} px={12}>
                <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
                    <Text fontSize='4xl'>Budget Dashboard</Text>

                    <Flex alignItems={'center'}>
                        <Stack direction={'row'} spacing={7}>
                            <Button onClick={toggleColorMode}>
                                {colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
                            </Button>
                        </Stack>
                    </Flex>
                </Flex>
            </Box>
            <SimpleGrid columns={2} spacing={10}>
                <Box m={12}><Select placeholder='Select Month'>
                    {month.map((m) => <option key={m} value={m}>{m}</option>)}

                </Select></Box>
                <Box m={12}><Select placeholder='Select Category'>
                    {category.map((m) => <option key={m} value={m}>{m}</option>)}
                </Select></Box>
                {/* <Box m={12}><Select placeholder='Select option'>
                    <option value='option1'>Option 1</option>
                    <option value='option2'>Option 2</option>
                    <option value='option3'>Option 3</option>
                </Select></Box> */}

            </SimpleGrid>
            <SimpleGrid columns={2} spacing={10}>
                <Box m={12} height={600}><MyResponsivePie data={pieChartDataMerchant} /></Box>
                <Box m={12} height={600}><MyResponsivePie data={pieChartDataCategory}/></Box>
            </SimpleGrid>


        </>
    );
}
