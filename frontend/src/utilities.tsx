import axios from "axios";

export const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/v1/",
});

// user registration async function 
export const userRegistration = async (email, password) => {
    let response = await api.post('users/register/', {
        email: email,
        password: password,
    });
    if (response.status === 201) {
        let { user, token } = response.data;
        localStorage.setItem("token", token);
        api.defaults.headers.common["Authorization"] = `Token ${token}`;
        return user;
    }
    alert(response.data);
    return null;
}

// user logout async function 
export const userLogout = async() => {
    let response = await api.post("/users/logout/");
    if (response.status === 204){
        localStorage.removeItem("token");
        delete api.defaults.headers.common["Authorization"];
        console.log("user logged out")
        return true;
    }
    alert("Logout failure.")
}