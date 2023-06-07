import React from "react";

import Grid from "@mui/material/Grid";
import Link from "@mui/material/Link";

export function LoginLink() {
    return (
        <Grid container justifyContent="flex-end">
            <Grid item>
                <Link href="#" variant="body2">
                    Уже есть аккаунт? Войти
                </Link>
            </Grid>
        </Grid>
    );
}
