import React from "react";

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";

import { Fields } from "./Fields.jsx";
import { AgreeTerms } from "./AgreeTerms.jsx";

export function Form() {
    return (
        <Box component="form" noValidate sx={{ mt: 3 }}>
            <Grid container spacing={2}>
                <Fields></Fields>
                <AgreeTerms></AgreeTerms>
            </Grid>
        </Box>
    );
}
