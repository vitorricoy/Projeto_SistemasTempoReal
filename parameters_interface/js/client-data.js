eel.get_parameters_and_random_client_data()(function (v) {
    console.log(v);
    let param = v[0];
    let decisionTimes = v[1];
    let perceptions = v[2];
    let latencies = v[3];
    let form = document.getElementById("parameters");
    for (let i = 1; i <= param.investors_num; i++) {
        let clientDiv = document.createElement("div");
        let button = document.createElement("button");
        button.type = "button";
        button.className = "collapsible";
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
        let balanceInput = document.createElement("input");
        balanceInput.id = "balance" + i;
        balanceInput.name = "balance" + i;
        balanceInput.type = "number";
        balanceInput.value = param.balance;
        balanceDiv.append(balanceLabel);
        balanceDiv.append(balanceInput);
        contentDiv.append(balanceDiv);

        let latencyDiv = document.createElement("div");
        let latencyLabel = document.createElement("label")
        latencyLabel.for = "latency" + i;
        latencyLabel.innerHTML = "Latency: ";
        let latencyInput = document.createElement("input");
        latencyInput.id = "latency" + i;
        latencyInput.name = "latency" + i;
        latencyInput.type = "number";
        latencyInput.value = latencies[i - 1];
        latencyDiv.append(latencyLabel);
        latencyDiv.append(latencyInput);
        contentDiv.append(latencyDiv);

        let decisionTimeDiv = document.createElement("div");
        let decisionTimeLabel = document.createElement("label")
        decisionTimeLabel.for = "decision-time" + i;
        decisionTimeLabel.innerHTML = "Decision time: ";
        let decisionTimeInput = document.createElement("input");
        decisionTimeInput.id = "decision-time" + i;
        decisionTimeInput.name = "decision-time" + i;
        decisionTimeInput.type = "number";
        decisionTimeInput.value = decisionTimes[i - 1];
        decisionTimeDiv.append(decisionTimeLabel);
        decisionTimeDiv.append(decisionTimeInput);
        contentDiv.append(decisionTimeDiv);

        let valuePerceptionModifierDiv = document.createElement("div");
        let valuePerceptionModifierLabel = document.createElement("label")
        valuePerceptionModifierLabel.for = "value-perception-modifier" + i;
        valuePerceptionModifierLabel.innerHTML = "Value perception modifier: ";
        let valuePerceptionModifierInput = document.createElement("input");
        valuePerceptionModifierInput.id = "value-perception-modifier" + i;
        valuePerceptionModifierInput.name = "value-perception-modifier" + i;
        valuePerceptionModifierInput.type = "number";
        valuePerceptionModifierInput.value = perceptions[i - 1];
        valuePerceptionModifierDiv.append(valuePerceptionModifierLabel);
        valuePerceptionModifierDiv.append(valuePerceptionModifierInput);
        contentDiv.append(valuePerceptionModifierDiv);

        let portfolioDiv = document.createElement("div");
        let portfolioLabel = document.createElement("label")
        portfolioLabel.for = "portfolio" + i;
        portfolioLabel.innerHTML = "Portifolio: ";
        let portfolioSelect = document.createElement("select");
        portfolioSelect.id = "portfolio" + i;
        portfolioSelect.name = "portfolio" + i;
        portfolioSelect.multiple = "true";
        for (let j = 1; j <= param.companies_num; j++) {
            let option = document.createElement("option");
            option.value = "STOCK" + j;
            option.innerHTML = "Company " + j;
            portfolioSelect.append(option);
        }
        portfolioDiv.append(portfolioLabel);
        portfolioDiv.append(portfolioSelect);
        contentDiv.append(portfolioDiv);

        let preferedStocksDiv = document.createElement("div");
        let preferedStocksLabel = document.createElement("label")
        preferedStocksLabel.for = "prefered-stocks" + i;
        preferedStocksLabel.innerHTML = "Prefered stocks: ";
        let preferedStocksUl = document.createElement("ul");
        preferedStocksUl.id = "prefered-stocks" + i;
        preferedStocksUl.name = "prefered-stocks" + i;
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
            li.innerHTML = "Company " + j;
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
    input.valeu = "Continuar";

    form.append(input);
});

const form = document.getElementById("parameters");

form.addEventListener("submit", function (event) {
    event.preventDefault();
    const FD = new FormData(form);
    let vals = Array.from(FD.entries());
    console.log(vals);
});