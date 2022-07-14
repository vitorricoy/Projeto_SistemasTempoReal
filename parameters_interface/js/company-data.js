var paramValues;

eel.get_parameters_and_prices()(function (v) {
    console.log(v);
    let param = v[0];
    let prices = v[1];
    paramValues = param;
    let form = document.getElementById("parameters");
    for (let i = 1; i <= param.companies_num; i++) {
        let priceDiv = document.createElement("div");
        let priceLabel = document.createElement("label")
        priceLabel.for = "price" + i;
        priceLabel.innerHTML = "Initial Price: ";
        priceLabel.className = "mdl-textfield__label";
        let priceInput = document.createElement("input");
        priceInput.id = "price" + i;
        priceInput.name = "price" + i;
        priceInput.type = "number";
        priceInput.step = "0.01";
        priceInput.value = prices[i - 1];
        priceInput.className = "mdl-textfield__input";
        priceDiv.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";
        priceDiv.append(priceLabel);
        priceDiv.append(priceInput);
        form.append(priceDiv);
    }
    let br = document.createElement("br");
    form.append(br);
    let input = document.createElement("input");
    input.type = "submit";
    input.value = "Executar";
    input.className = "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored";

    form.append(input);
});

const form = document.getElementById("parameters");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    let companiesData = []

    for (let i = 1; i <= paramValues.companies_num; i++) {

        let companyData = {
            price: parseFloat(document.getElementById("price" + i).value)
        };

        companiesData.push(companyData);
    }
    eel.set_company_data(companiesData)(function () {
        window.close();
    });
});