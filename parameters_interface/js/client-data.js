var paramValues;

eel.get_parameters_and_random_client_data()(function (v) {
    console.log(v);
    let param = v[0];
    paramValues = param;
    let decisionTimes = v[1];
    let perceptions = v[2];
    let latencies = v[3];
    let form = document.getElementById("parameters");
    for (let i = 1; i <= param.investors_num; i++) {
        let clientDiv = document.createElement("div");
        let button = document.createElement("button");
        button.type = "button";
        button.className = "collapsible mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--colored";
        button.innerHTML = "Client " + i;

        button.addEventListener("click", function () {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });

        clientDiv.append(button);

        let contentDiv = document.createElement("div");
        contentDiv.className = "content";

        let balanceDiv = document.createElement("div");
        let balanceLabel = document.createElement("label")
        balanceLabel.for = "balance" + i;
        balanceLabel.innerHTML = "Balance: ";
        balanceLabel.className = "mdl-textfield__label";
        let balanceInput = document.createElement("input");
        balanceInput.id = "balance" + i;
        balanceInput.name = "balance" + i;
        balanceInput.type = "number";
        balanceInput.step = "0.01";
        balanceInput.value = param.balance;
        balanceInput.className = "mdl-textfield__input";
        balanceDiv.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";
        balanceDiv.append(balanceLabel);
        balanceDiv.append(balanceInput);
        contentDiv.append(balanceDiv);

        let latencyDiv = document.createElement("div");
        let latencyLabel = document.createElement("label")
        latencyLabel.for = "latency" + i;
        latencyLabel.innerHTML = "Latency: ";
        latencyLabel.className = "mdl-textfield__label";
        let latencyInput = document.createElement("input");
        latencyInput.id = "latency" + i;
        latencyInput.name = "latency" + i;
        latencyInput.type = "number";
        latencyInput.step = "0.01";
        latencyInput.value = latencies[i - 1];
        latencyInput.className = "mdl-textfield__input";
        latencyDiv.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";
        latencyDiv.append(latencyLabel);
        latencyDiv.append(latencyInput);
        contentDiv.append(latencyDiv);

        let decisionTimeDiv = document.createElement("div");
        let decisionTimeLabel = document.createElement("label")
        decisionTimeLabel.for = "decision-time" + i;
        decisionTimeLabel.innerHTML = "Decision time: ";
        decisionTimeLabel.className = "mdl-textfield__label";
        let decisionTimeInput = document.createElement("input");
        decisionTimeInput.id = "decision-time" + i;
        decisionTimeInput.name = "decision-time" + i;
        decisionTimeInput.type = "number";
        decisionTimeInput.step = "0.01";
        decisionTimeInput.value = decisionTimes[i - 1];
        decisionTimeInput.className = "mdl-textfield__input";
        decisionTimeDiv.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";
        decisionTimeDiv.append(decisionTimeLabel);
        decisionTimeDiv.append(decisionTimeInput);
        contentDiv.append(decisionTimeDiv);

        let valuePerceptionModifierDiv = document.createElement("div");
        let valuePerceptionModifierLabel = document.createElement("label")
        valuePerceptionModifierLabel.for = "value-perception-modifier" + i;
        valuePerceptionModifierLabel.innerHTML = "Value perception modifier: ";
        valuePerceptionModifierLabel.className = "mdl-textfield__label";
        let valuePerceptionModifierInput = document.createElement("input");
        valuePerceptionModifierInput.id = "value-perception-modifier" + i;
        valuePerceptionModifierInput.name = "value-perception-modifier" + i;
        valuePerceptionModifierInput.type = "number";
        valuePerceptionModifierInput.step = "0.01";
        valuePerceptionModifierInput.value = perceptions[i - 1];
        valuePerceptionModifierInput.className = "mdl-textfield__input";
        valuePerceptionModifierDiv.append(valuePerceptionModifierLabel);
        valuePerceptionModifierDiv.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";
        valuePerceptionModifierDiv.append(valuePerceptionModifierInput);
        contentDiv.append(valuePerceptionModifierDiv);

        let portifolioDiv = document.createElement("div");
        let portifolioLabel = document.createElement("label")
        portifolioLabel.for = "portifolio" + i;
        portifolioLabel.innerHTML = "Portifolio: ";
        let portifolioSelect = document.createElement("select");
        portifolioSelect.id = "portifolio" + i;
        portifolioSelect.name = "portifolio" + i;
        portifolioSelect.multiple = "true";
        portifolioSelect.style = "width: 80%";
        for (let j = 1; j <= param.companies_num; j++) {
            let option = document.createElement("option");
            option.value = "STOCK" + j;
            option.innerHTML = "Company " + j;
            portifolioSelect.append(option);
        }
        portifolioDiv.append(portifolioLabel);
        portifolioDiv.append(portifolioSelect);
        contentDiv.append(portifolioDiv);

        let preferedStocksDiv = document.createElement("div");
        let preferedStocksLabel = document.createElement("label")
        preferedStocksLabel.for = "prefered-stocks" + i;
        preferedStocksLabel.innerHTML = "Prefered stocks: ";
        let preferedStocksUl = document.createElement("ul");
        preferedStocksUl.id = "prefered-stocks" + i;
        preferedStocksUl.name = "prefered-stocks" + i;
        preferedStocksUl.className = "mdl-list";
        Sortable.create(preferedStocksUl);
        let companiesIndexes = [];
        for (let j = 1; j <= param.companies_num; j++) {
            companiesIndexes.push(j);
        }
        let shuffledCompaniesIndexes = companiesIndexes
            .map(value => ({ value, sort: Math.random() }))
            .sort((a, b) => a.sort - b.sort)
            .map(({ value }) => value);
        console.log(companiesIndexes);
        console.log(shuffledCompaniesIndexes);
        for (let j of shuffledCompaniesIndexes) {
            let li = document.createElement("li");
            li.innerHTML = "<svg enable-background='new 0 0 24 24' height='12' viewBox='2.612 0 18.341 7.661' width='24' xmlns='http://www.w3.org/2000/svg'><g><rect fill='none' height='24' width='24'/></g><g transform='matrix(1, 0, 0, 1, -0.029021, -8.386941)'><g><g><path d='M20,9H4v2h16V9z M4,15h16v-2H4V15z'/></g></g></g></svg><p style='margin-bottom: 0px; margin-left: 15px;'>Company " + j + "</p>";
            li.className = "mdl-list__item";
            preferedStocksUl.append(li);
        }
        preferedStocksDiv.append(preferedStocksLabel);
        preferedStocksDiv.append(preferedStocksUl);
        contentDiv.append(preferedStocksDiv);

        clientDiv.append(contentDiv);

        form.append(clientDiv);
    }

    let input = document.createElement("input");
    input.type = "submit";
    input.value = "Continuar";
    input.className = "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored";

    form.append(input);

    var selectScript = document.createElement('script');
    selectScript.setAttribute('src', 'js/multi-select-dropdown.js');
    document.body.appendChild(selectScript);
});

const form = document.getElementById("parameters");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    let clientsData = []

    let companyValueIDMap = {};
    for (let i = 1; i <= paramValues.companies_num; i++) {
        companyValueIDMap['Company ' + i] = "STOCK" + (i - 1);
    }

    for (let i = 1; i <= paramValues.investors_num; i++) {
        let portifolio = Array.prototype.slice.call(document.querySelectorAll('#portifolio' + i + ' option:checked'), 0).map(function (v, i, a) {
            return v.value;
        });
        let preferedStocks = [];
        let element = document.getElementById("prefered-stocks" + i);
        for (let child of element.children) {
            let text = child.querySelector("p");
            preferedStocks.push(companyValueIDMap[text.innerHTML]);
        }

        let clientData = {
            balance: parseFloat(document.getElementById("balance" + i).value),
            latency: parseFloat(document.getElementById("latency" + i).value),
            decision_time: parseFloat(document.getElementById("decision-time" + i).value),
            value_perception_modifier: parseFloat(document.getElementById("value-perception-modifier" + i).value),
            portifolio: portifolio,
            prefered_stocks: preferedStocks
        };

        clientsData.push(clientData);
    }
    eel.set_client_data(clientsData)(function () {
        window.close();
    });
});