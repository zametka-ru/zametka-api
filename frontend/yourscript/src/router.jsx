import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { Register } from "./views/auth/Register.jsx";

export const router = createBrowserRouter([
    {
        path: "/signup",
        element: <Register></Register>,
    },
]);
