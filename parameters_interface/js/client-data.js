var paramValues;

eel.get_parameters_and_random_client_data()(function (v) {
    let param = v[0];
    paramValues = param;
    let decisionTimes = v[1];
    let perceptions = v[2];
    let latencies = v[3];
    let form = document.getElementById("parameters");
    let accordion = document.createElement("div");
    accordion.id = "the-accordion";
    accordion.className = "accordion-wrapper";
    for (let i = 1; i <= param.investors_num; i++) {
        let accordionPanel = document.createElement("div");
        accordionPanel.className = "accordion-panel";
        let clientDiv = document.createElement("div");
        clientDiv.className = "accordion-title";
        let title = document.createElement("a");
        title.href = "#";
        title.innerHTML = "Client " + i;
        clientDiv.append(title);

        let contentDiv = document.createElement("div");
        contentDiv.className = "accordion-content";

        let balanceDiv = document.createElement("div");
        let balanceLabel = document.createElement("label")
        balanceLabel.for = "balance" + i;
        balanceLabel.innerHTML = "Balance ($): ";
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
        latencyLabel.innerHTML = "Latency (ms): ";
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
        decisionTimeLabel.innerHTML = "Decision time (ms): ";
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

        let valuePerceptionDiv = document.createElement("div");
        valuePerceptionDiv.style = "display: flex; flex-direction: column;";
        let valuePerceptionText = document.createElement("p");
        valuePerceptionText.innerHTML = "Value perception: ";
        valuePerceptionText.className = "mdl-typography--subhead";
        valuePerceptionDiv.append(valuePerceptionText);

        for (let j = 1; j <= param.companies_num; j++) {
            let valuePerceptionRow = document.createElement("div");
            let valuePerceptionLabel = document.createElement("label")
            valuePerceptionLabel.for = "value-perception-" + i + "-stock" + (j - 1);
            valuePerceptionLabel.innerHTML = "Value perception for stock STOCK " + (j - 1) + " (%): ";
            valuePerceptionLabel.className = "mdl-textfield__label";

            let valuePerceptionOfStock = document.createElement("input");
            valuePerceptionOfStock.id = "value-perception-" + i + "-stock" + (j - 1);
            valuePerceptionOfStock.name = "value-perception-" + i + "-stock" + (j - 1);
            valuePerceptionOfStock.type = "number";
            valuePerceptionOfStock.step = "0.01";
            valuePerceptionOfStock.className = "mdl-textfield__input";
            valuePerceptionOfStock.value = perceptions[i - 1];
            valuePerceptionRow.append(valuePerceptionLabel);

            valuePerceptionRow.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";
            valuePerceptionRow.append(valuePerceptionOfStock);

            valuePerceptionDiv.append(valuePerceptionRow);
        }
        /*let valuePerceptionModifierLabel = document.createElement("label")
        valuePerceptionModifierLabel.for = "value-perception-modifier" + i;
        valuePerceptionModifierLabel.innerHTML = "Value perception modifier (%): ";
        valuePerceptionModifierLabel.className = "mdl-textfield__label";*/
        /*let valuePerceptionModifierInput = document.createElement("input");
        valuePerceptionModifierInput.id = "value-perception-modifier" + i;
        valuePerceptionModifierInput.name = "value-perception-modifier" + i;
        valuePerceptionModifierInput.type = "number";
        valuePerceptionModifierInput.step = "0.01";
        valuePerceptionModifierInput.value = perceptions[i - 1];
        valuePerceptionModifierInput.className = "mdl-textfield__input";
        valuePerceptionModifierDiv.append(valuePerceptionModifierLabel);
        valuePerceptionModifierDiv.className = "mdl-textfield mdl-js-textfield mdl-textfield--floating-label";
        valuePerceptionModifierDiv.append(valuePerceptionModifierInput);*/
        contentDiv.append(valuePerceptionDiv);

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
            option.value = "STOCK" + (j - 1);
            option.innerHTML = "Company " + j;
            // option.selected = true;
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
        for (let j of shuffledCompaniesIndexes) {
            let li = document.createElement("li");
            li.innerHTML = "<svg enable-background='new 0 0 24 24' height='12' viewBox='2.612 0 18.341 7.661' width='24' xmlns='http://www.w3.org/2000/svg'><g><rect fill='none' height='24' width='24'/></g><g transform='matrix(1, 0, 0, 1, -0.029021, -8.386941)'><g><g><path d='M20,9H4v2h16V9z M4,15h16v-2H4V15z'/></g></g></g></svg><p style='margin-bottom: 0px; margin-left: 15px;'>Company " + j + "</p>";
            li.className = "mdl-list__item";
            preferedStocksUl.append(li);
        }
        preferedStocksDiv.append(preferedStocksLabel);
        preferedStocksDiv.append(preferedStocksUl);
        contentDiv.append(preferedStocksDiv);

        accordionPanel.append(clientDiv);
        accordionPanel.append(contentDiv);

        accordion.append(accordionPanel);
    }

    form.append(accordion);

    let selectScript = document.createElement('script');
    selectScript.setAttribute('src', 'js/multi-select-dropdown.js');
    document.body.appendChild(selectScript);

    let accordionCss = document.createElement('link');
    accordionCss.rel = "stylesheet";
    accordionCss.href = "css/accordionjs.min.css";
    document.body.appendChild(accordionCss);

    let accordionMinScript = document.createElement('script');
    accordionMinScript.charset = "utf-8";
    accordionMinScript.src = "js/accordionjs.min.js";
    accordionMinScript.onload = () => {
        let accordionScript = document.createElement('script');
        accordionScript.type = "text/javascript";
        accordionScript.innerHTML = "(function(){ new window.AccordionJS();})();";
        document.body.appendChild(accordionScript);
    };
    document.body.appendChild(accordionMinScript);

});

eel.get_parameters_and_prices()(function (v) {
    let param = v[0];
    let prices = v[1];
    paramValues = param;
    let form = document.getElementById("parameters");
    let br1 = document.createElement("br");
    form.append(br1);
    for (let i = 1; i <= param.companies_num; i++) {
        let priceDiv = document.createElement("div");
        let priceLabel = document.createElement("label")
        priceLabel.for = "price" + i;
        priceLabel.innerHTML = "Company " + i + " Initial Value: ";
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

    let clientsData = [];

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
        let values_perceptions = {};
        for (let j = 1; j <= paramValues.companies_num; j++) {
            const key = companyValueIDMap['Company ' + j];

            const value = parseFloat(document.getElementById("value-perception-" + i + "-stock" + (j - 1)).value);
            values_perceptions[key] = value / 100;
        }

        console.log(values_perceptions);

        let clientData = {
            balance: parseFloat(document.getElementById("balance" + i).value),
            latency: parseFloat(document.getElementById("latency" + i).value),
            decision_time: parseFloat(document.getElementById("decision-time" + i).value),
            values_perceptions: values_perceptions,
            //value_perception_modifier: parseFloat(document.getElementById("value-perception-modifier" + i).value),
            portifolio: portifolio,
            prefered_stocks: preferedStocks
        };

        clientsData.push(clientData);
    }
    eel.set_client_data(clientsData, companiesData)(function () {
        window.close();
    });
});