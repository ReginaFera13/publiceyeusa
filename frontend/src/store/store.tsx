import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./authSlice";
import profileReducer from "./profileSlice";
import affiliationsReducer from "./affiliationsSlice";

const store = configureStore({
  reducer: {
    auth: authReducer,
    profile: profileReducer,
    affiliations: affiliationsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;