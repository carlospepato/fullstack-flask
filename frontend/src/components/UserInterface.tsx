import React, {useState, useEffect} from "react";
import axios from "axios";
import CardComponent from "./CardComponent";

interface User{
    id: number;
    email: string;
    name: string;
}

interface UserInterfaceProps{
    BackendName: string;
}

const UserInterface: React.FC<UserInterfaceProps> = ({ BackendName }) => {

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    const [users, setUsers] = React.useState<User[]>([]);
    const [newUser, setNewUser] = React.useState<User>({id: 0, email: '', name: ''});
    const [updateUser, setUpdateUser] = React.useState<User>({id: 0, email: '', name: ''});

    const backgroundColor: { [ key: string ]: string } = {
        flask: 'bg-blue-500',
    };
    
    const buttonColors: { [ key: string ]: string } = {
        flask: 'bg-ble-700 hover:bg-blue-600',
    };

    const bgColor = backgroundColor[BackendName as keyof typeof backgroundColor] || 'bg-gray-500';
    const btnColor = buttonColors[BackendName as keyof typeof buttonColors] || 'bg-ble-700 hover:bg-blue-600';

    //fetch users
    useEffect(() => {
        const fetchData = async () => {
            try{
                const response = await axios.get(`${apiUrl}/api/${BackendName}/users`);
                setUsers(response.data.reverse());
            }catch(error){
                console.log('Error: ', error);
            }
        };

        fetchData();
    }, [BackendName, apiUrl]);

    return (
       <div className={`user-interface ${bgColor} ${BackendName} w-full max-w-md p-4 my-4 rounded shadow`}>
        <img src={`/${BackendName} logo.svg`} alt={`${BackendName} Logo`} className="w-20 h-20 mb-6 mx-auto" />
        <h2 className="text-xl font-bold text-center text-white mb-6">{`${BackendName.charAt(0).toUpperCase() + BackendName.slice(1)} Backend`}</h2>
       
       {/* Display users*/}
        <div className="space-y-4">
        {users.map((user) => (
            <div key={user.id} className="flex items-center justify-between bg-white p-4">
                <CardComponent card={user} />
                <button onClick={() => deleteUser(user.id)} className={`${btnColor} `}>Delete User</button>
            </div>
        ))}
       </div>
       </div>
    );
};
export default UserInterface;