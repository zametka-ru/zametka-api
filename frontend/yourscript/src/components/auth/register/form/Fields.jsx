import React from "react";

import { Input } from "./Input.jsx";

export function Fields() {
    const fields = [
        {
            autocomplete: "given-name",
            name: "firstName",
            id: "firstName",
            label: "Имя",
            autofocus: true,
            sm: 6,
        },
        {
            autocomplete: "family-name",
            name: "lastName",
            id: "lastName",
            label: "Фамилия",
            sm: 6,
        },
        {
            autocomplete: "email",
            name: "email",
            id: "email",
            label: "Почта",
        },
        {
            autocomplete: "new-password",
            name: "password",
            id: "password",
            label: "Пароль",
        },
        {
            name: "password2",
            id: "password2",
            label: "Пароль еще раз",
        },
    ];

    return fields.map((field) => (
        <Input
            key={field.id}
            name={field.name}
            autofocus={field.autofocus}
            autocomplete={field.autocomplete}
            id={field.id}
            label={field.label}
            sm={field.sm}
        ></Input>
    ));
}
