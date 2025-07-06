import React from 'react'
import styles from "./styles.module.css"

const {logo} = styles
const Heading = () => {
    return (
        <h2 className={logo}>Dish<span>Dash</span>🍽️</h2>
    )
}

export default Heading