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
    const [params, setParams] = useState({});
    const [selectedMonth, setSelectedMonth] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState([]);


    useEffect(() => {

        const parsedParams = { "month": selectedMonth, "category": selectedCategory }
        if (Object.keys(selectedMonth).length >= 1) {

            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
                mode: 'cors',
                body: JSON.stringify({ 'month': selectedMonth, 'category': selectedCategory })
            };
            fetch('http://127.0.0.1:5000/home', requestOptions)
                .then((response) => response.json())
                .then((actualData) => {
                    setPieChartDataMerchant(actualData[0]['pie_chart_data_merchant'])
                    setPieChartDataCategory(actualData[0]['pie_chart_data_category'])
                    console.log("pie_chart_data_merchant", actualData[0]['pie_chart_data_merchant'])
                    console.log("pie_chart_data_category", actualData[0]['pie_chart_data_category'])
                    setLoading(false)
                    setError(null)
                })
                .catch((err) => {
                    console.log(err.message);
                });

        }
        else {
            fetch(`http://127.0.0.1:5000/default`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
                mode: 'cors',

            })
                .then((response) => response.json())
                // .then((actualData) => setMonth(actualData[0]['month']))
                .then((actualData) => {
                    setMonth(actualData[0]['month'])
                    setCategory(actualData[0]['category'])
                    setError(null);
                    console.log("month", month)
                    console.log("category", category)
                    setLoading(false)
                })
                .catch((err) => {
                    console.log(err.message);
                });
            console.log("selectedMonth", selectedMonth, selectedCategory)
        }
        console.log("selectedMonth", selectedMonth);
        console.log("length of selectedMonth", Object.keys(selectedMonth).length)
    }, [selectedMonth, selectedCategory]);

    function resetf(e){
        console.log("reset button clicked")
        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
            mode: 'cors',
        };
        fetch('http://127.0.0.1:5000/home', requestOptions)
            .then((response) => response.json())
            .then((actualData) => {
                setPieChartDataMerchant(actualData[0]['pie_chart_data_merchant'])
                setPieChartDataCategory(actualData[0]['pie_chart_data_category'])
                console.log("pie_chart_data_merchant", actualData[0]['pie_chart_data_merchant'])
                console.log("pie_chart_data_category", actualData[0]['pie_chart_data_category'])
                setLoading(false)
                setError(null)
            })
            .catch((err) => {
                console.log(err.message);
            });
    }

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
            <Flex columns={3} >
            <Box m={12}></Box><Box m={12}></Box><Box m={12}></Box><Box m={12}></Box><Box m={12}></Box><Box m={12}></Box>
                <Box m={12}><Select onChange={(e) => setSelectedMonth(e.target.value)} placeholder='Select Month'>
                    {month.map((m) => <option key={m} value={m}>{m}</option>)}

                </Select></Box>
                <Box m={12}><Select onChange={(e) => setSelectedCategory(e.target.value)} placeholder='Select Category' >
                    {category.map((m) => <option key={m} value={m}>{m}</option>)}
                </Select></Box>
                <Box m={8}>
                <Button colorScheme='teal' size='md' sx={{ margin: "4" }} onClick={resetf}> Reset </Button>
                </Box>
            </Flex>
            
            <SimpleGrid columns={2} spacing={10}>
                <Box m={12} height={600}><MyResponsivePie data={pieChartDataMerchant} colorScheme="nivo"/></Box>
                <Box m={12} height={600}><MyResponsivePie data={pieChartDataCategory} colorScheme="paired"/></Box>
            </SimpleGrid>


        </>
    );
}
