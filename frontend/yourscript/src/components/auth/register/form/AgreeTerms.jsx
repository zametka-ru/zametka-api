import React from "react";

import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Grid from "@mui/material/Grid";

export function AgreeTerms() {
    return (
        <Grid item xs={12}>
            <FormControlLabel
                control={<Checkbox value="agreeTerms" color="primary" />}
                label="Я соглашаюсь с ToS и обещаю их соблюдать."
            />
        </Grid>
    );
}
