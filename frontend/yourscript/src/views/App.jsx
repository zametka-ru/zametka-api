import React from "react";

import { RouterProvider } from "react-router-dom";

import { router } from "../router.jsx";

import CssBaseline from "@mui/material/CssBaseline";

import { createTheme, ThemeProvider } from "@mui/material/styles";

export function App() {
    const theme = createTheme({
        palette: {
            mode: "light",
            primary: {
                main: "#1F5673",
            },
            secondary: {
                main: "#759FBC",
            },
        },
    });

    return (
        <CssBaseline>
            <RouterProvider router={router} />
        </CssBaseline>
    );
}
