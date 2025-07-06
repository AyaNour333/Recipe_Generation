import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

const actPostInput = createAsyncThunk("recipeSlice/actPostInput",
    async(input , thunkAPI)=>{
        const {rejectWithValue} = thunkAPI
        try{
            console.log("hi");
            
            const response = await axios.post("http://127.0.0.1:8000/recommend-recipe", {
                user_input: input  
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log("Response from backend:", response);
            return response.data
        }
        catch(error){
            return rejectWithValue("error not found")
        }
    })

export default actPostInput