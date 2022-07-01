// Access the form element...
const form = document.getElementById("parameters");

// ...and take over its submit event.
form.addEventListener("submit", function (event) {
    event.preventDefault();
    const FD = new FormData(form);
    let vals = Array.from(FD.entries());
    let parameters = {};
    for (let val of vals) {
        parameters[val[0]] = parseInt(val[1]);
    }
    eel.set_values(parameters)(function () {
        window.close();
    });
});

