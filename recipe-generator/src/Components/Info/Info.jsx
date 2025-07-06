import React from 'react'
import styles from './styles.module.css'
import Tree from '../../assets/imgs/wing.png'

const {working , steps , step,image} = styles
const Info = () => {
    return (
        <div className={`${working} d-flex flex-column align-items-center`}>
            <span>cooking up ,baby</span>
            <h2>How it works</h2>
            <p>What if your ingredients could think for themselves? Our AI engine does just that . turning your inputs into delicious, personalized recipes.</p>
            <div className={`${steps} flex-column`}>
                <div className={step}>
                    <img className={image} src={Tree} alt="" />  
                    <div>
                        <h3>Enter a Prompt</h3>
                        <p>Just enter the ingredients you have on hand, and our tool will generate a recipe for you. You can also specify dietary preferences like vegan, vegetarian, and even add your mood or emotions to make the recipe more personalized.</p>
                    </div>
                </div>
                <div className={step}>
                    <img className={image} src={Tree} alt="" />
                    <div>
                        <h3>DishDash Generates</h3>
                        <p>DishDash uses AI to instantly generate a unique recipe based on your ingredients, complete with a title, ingredients list, and easy-to-follow steps.</p>
                    </div>
                </div>
                <div className={step}>
                    <h3>Note</h3>
                    <div>
                        <p>To get the most accurate and personalized recipe, please be as specific and detailed as possible when entering your ingredients and preferences. The more information you provide, the better the recipe will suit your needs!</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Info