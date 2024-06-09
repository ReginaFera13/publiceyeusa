import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import api from "../utilities";

type User = {
    email: string;
    password: string;
};

type UserBasicInfo ={
    id: string;
    name: string;
    email: string;
};

type userProfileData = {
    name: string;
    email: string;
};

type AuthState = {
    basicUserInfo?: UserBasicInfo | null;
    userProfileData?: userProfileData | null;
    status: 'idle' | 'loading' | 'failed';
    error: string | null;
};

const initialState: AuthState = {
    basicUserInfo: localStorage.getItem('token')
        ? JSON.parse(localStorage.getItem('token') as string)
        : null,
    userProfileData: undefined,
    status: 'idle',
    error: null,
};

export const login = createAsyncThunk('login', async (data: User) => {
    const response = await api.post("users/login/", data);

    if (response.status === 200) {
        let { user, token } = response.data;
        localStorage.setItem("token", token);
        api.defaults.headers.common["Authorization"] = `Token ${token}`;
        return user;
    }
    alert('Invalid Login Credentials');
    return null;
});

export const register = createAsyncThunk('register', async (data: User) => {
    let response = await api.post('users/register/', data);
    if (response.status === 201) {
        let { user, token } = response.data;
        localStorage.setItem("token", token);
        api.defaults.headers.common["Authorization"] = `Token ${token}`;
        return user;
    }
    alert(response.data);
    return null;
})

const authSlice = createSlice({
  name: "auth",
  initialState: "",
  reducers: {},
});

export default authSlice.reducer;