import React from "react";

import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";

export function Input({
    autocomplete = undefined,
    name,
    id,
    label,
    autofocus = undefined,
    sm = undefined,
}) {
    return (
        <Grid item xs={12} sm={sm}>
            <TextField
                autoComplete={autocomplete}
                name={name}
                required
                fullWidth
                id={id}
                label={label}
                autoFocus={autofocus}
            />
        </Grid>
    );
}
