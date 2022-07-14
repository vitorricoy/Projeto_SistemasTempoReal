var paramValues;

eel.get_parameters_and_prices()(function (v) {
    console.log(v);
    let param = v[0];
    let prices = v[1];
    paramValues = param;
    let form = document.getElementById("parameters");
    for (let i = 1; i <= param.companies_num; i++) {
        let company = document.createElement("div");
        let button = document.createElement("button");
        button.type = "button";
        button.className = "collapsible";
        button.innerHTML = "Company " + i;

        button.addEventListener("click", function () {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });

        company.append(button);

        let contentDiv = document.createElement("div");
        contentDiv.className = "content";

        let priceDiv = document.createElement("div");
        let priceLabel = document.createElement("label")
        priceLabel.for = "price" + i;
        priceLabel.innerHTML = "Initial Price: ";
        let priceInput = document.createElement("input");
        priceInput.id = "price" + i;
        priceInput.name = "price" + i;
        priceInput.type = "number";
        priceInput.step = "0.01";
        priceInput.value = prices[i - 1];
        priceDiv.append(priceLabel);
        priceDiv.append(priceInput);
        contentDiv.append(priceDiv);

        company.append(contentDiv);

        form.append(company);
    }

    let input = document.createElement("input");
    input.type = "submit";
    input.value = "Executar";

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