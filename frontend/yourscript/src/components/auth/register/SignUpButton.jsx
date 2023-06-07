import React from "react";

import Button from "@mui/material/Button";

export function SignUpButton() {
    return (
        <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
        >
            Зарегистрироваться
        </Button>
    );
}
