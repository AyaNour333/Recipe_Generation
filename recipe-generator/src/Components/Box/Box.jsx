import styles from  './styles.module.css'

const Box = ({ title, data }) => {
    let listItems = [];

    if (Array.isArray(data)) {
        listItems = data;
    } else if (typeof data === 'string') {
        const cleaned = data
            .replace(/[\[\]']+/g, "") 
            .split(title.toLowerCase() === 'directions' ? '.' : ',') 
            .map(item => item.trim().replace(/^,|,$/g, '')) 
            .filter(Boolean); // remove empty strings
        listItems = cleaned;
    }

    return (
        <div className={styles.box}>
            <h2>{title}</h2>
            <ol>
                {listItems.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ol>
        </div>
    );
};

export default Box