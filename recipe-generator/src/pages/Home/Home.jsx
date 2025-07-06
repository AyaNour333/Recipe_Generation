import { useState } from 'react'
import { Info, Recipe } from '../../Components'
import styles from './styles.module.css'
import { Button, Container, Form } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { actPostInput } from '../../store/recipes/recipeSlice'
import Loading from '../../Components/feedback/Loading'

const {page , input , btn , the_form, heading , emotion_message} = styles
const Home = () => {
    const dispatch = useDispatch()
    const [inputValue , setInputValue] = useState("")
    const {recipes , loading , message} = useSelector(state => state.recipes)
    return (
        <>
        <div className={page}>
            <h2 className={heading}>Generate A Lovely Recipe</h2>
            <Container style={{position: "relative" , zIndex: 2}}>
                <Form className= {`d-flex justify-content-center align-items-center flex-column ${the_form}`}
                onSubmit={(e)=>{
                    e.preventDefault();
                    dispatch(actPostInput(inputValue))
                    }}>
                    <Form.Control type='text' className={input}
                    onInput={e => setInputValue(e.target.value)}
                    />
                    <Button className={btn} type='submit'>Generate</Button>
                </Form>
                <Loading status={loading}>
                    {message?.length>0 && <div className={emotion_message}>{message}</div>}
                    {recipes.length>0 && recipes.map(el => <Recipe key={el.title}
                    recipeTitle={el.title}
                    ingredients={el.ingredients}
                    directions={el.directions}
                    calories={el.calories} />)
                    }
                </Loading> 
            </Container>
        </div>
        <Info/>
        </>
    )
}

export default Home