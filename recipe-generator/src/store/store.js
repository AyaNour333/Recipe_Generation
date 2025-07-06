import { configureStore } from "@reduxjs/toolkit";
import recipeSlice from './recipes/recipeSlice'

export const store = configureStore({
    reducer:{
        recipes : recipeSlice
    }
})

