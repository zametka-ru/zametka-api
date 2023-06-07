import React from "react";

import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";

export function Copyright({ title, href, sx }) {
    return (
        <Typography
            variant="body2"
            color="text.secondary"
            align="center"
            sx={sx}
        >
            {"Все права защищены © "}
            <Link color="inherit" href={href}>
                {title}
            </Link>{" "}
            {new Date().getFullYear()}
            {"."}
        </Typography>
    );
}
