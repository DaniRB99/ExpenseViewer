import { useState, type JSX } from "react";

export interface ILikes {
    likes: number,
    increaseLikes: () => void
}

function DetailsWrapper(props: {
    render: (likes:number,
        increaseLikes:()=>void) => JSX.Element
}) {
    const [likes, setLikes] = useState(0);

    const increaseLikes = () => {
        setLikes(likes + 1);
    }

    return <>{props.render(likes, increaseLikes)}</>
}

export default DetailsWrapper