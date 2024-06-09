import ReactDOM from 'react-dom/client'
import { RouterProvider } from "react-router-dom";
import { Provider } from 'react-redux';
import router from "./router";
import './index.css'
import store from './store/store';

ReactDOM.createRoot(document.getElementById('root')!).render(
    <Provider store={store}>
        <RouterProvider router={router} />
    </Provider>
)
