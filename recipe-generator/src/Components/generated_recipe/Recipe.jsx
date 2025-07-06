import React from 'react'
import Box from '../Box/Box'
import styles from  './styles.module.css'

const {recipeBox , cal} = styles
const Recipe = ({recipeTitle , ingredients , directions , calories}) => {
        return (
            <div className={recipeBox}>
                <h2>{recipeTitle}</h2>
                <div className='d-flex column-gap-4'>
                    <Box title="ingredients" data={ingredients}/>
                    <Box title="directions" data={directions}/>
                </div>
                <div className={cal}><span>Calories</span> : {calories}</div>
            </div>
        )
    }
    
export default Recipe