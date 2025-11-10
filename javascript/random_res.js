function onToggleRandomRes(enabled) {
    const button = document.getElementById("random_resolution_toggle");

    button.style.background = `var(--button-${enabled ? 'primary' : 'secondary'}-background-fill)`;
    button.title = `Random Resolution: ${enabled ? 'Enabled' : 'Disabled'}`;
}

onUiLoaded(() => {
    const row = document.getElementById("txt2img_dimensions_row");
    const button = document.getElementById("random_resolution_toggle");

    button.style.background = "var(--button-secondary-background-fill);";
    button.title = "Random Resolution: Disabled";
    row.appendChild(button);
});
