import React from "react";
import UserInterface from "../components/UserInterface";

const Home: React.FC = () => {
    return (
        <div>
            <UserInterface BackendName="flask"/>
        </div>
    )
}

export default Home;