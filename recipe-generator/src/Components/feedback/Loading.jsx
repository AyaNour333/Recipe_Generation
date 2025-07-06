import Lottie from "lottie-react"
import loading from '../../assets/LottieFiles/Loading.json'
import styles from './styles.module.css'

const {load} = styles
const Loading = ({children,status}) => {
    if(status === "pending"){
        return <Lottie animationData={loading} 
        style={{width:"200px"}} className={load}/>
    }
    return (
        <>
            {children}
        </>
    )
}

export default Loading