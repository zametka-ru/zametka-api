import React from "react";

import { Icon } from "./Icon.jsx";
import { Title } from "./Title.jsx";

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";

import { Form } from "./form/Form.jsx";
import { Copyright } from "./Copyright.jsx";
import { SignUpButton } from "./SignUpButton.jsx";
import { LoginLink } from "./LoginLink.jsx";

export function Register() {
    return (
        <Container maxWidth="xs">
            <Box
                sx={{
                    marginTop: 8,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                <Icon></Icon>
                <Title></Title>
                <Form></Form>
                <SignUpButton></SignUpButton>
                <LoginLink></LoginLink>
            </Box>
            <Copyright
                sx={{ mt: 3 }}
                title="yourscript"
                href="https://github.com/lubaskinc0de/yourscript"
            />
        </Container>
    );
}
