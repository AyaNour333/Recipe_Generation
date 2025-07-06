import { createSlice } from "@reduxjs/toolkit";
import actPostInput from "./act/actPostInput";

const initialState = {
    recipes: [],
    message: "",
    loading: "idle",
    error: null
}
const recipeSlice = createSlice({
    initialState,
    name:"recipeSlice",
    reducers:{},
    extraReducers:(builder)=>{
        builder.addCase(actPostInput.pending, (state) =>{
            state.loading = "pending"
            state.error = "null"
        })
        builder.addCase(actPostInput.fulfilled , (state , action)=>{
            state.loading = "succeeded"
            state.recipes = action.payload.recipes
            state.message = action.payload.message
        })
        builder.addCase(actPostInput.rejected , (state , action)=>{
            state.loading = "failed"
            state.error = action.payload
        })
    }
})

export {actPostInput}
export default recipeSlice.reducer