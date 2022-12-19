function elementWithText(tag, text) {
    const e = document.createElement(tag);
    e.innerText = text;
    return e;
}

const taskKeys = ["id", "created", "finished", "result"];

const generateTableHeader = () => {
    const thead = document.createElement("thead");
    const tr = document.createElement("tr");
    for (let key of taskKeys) {
        tr.appendChild(elementWithText("th", key));
    }
    thead.appendChild(tr);
    return thead;
}

const removeAllChildren = (e) => {
    while (e.firstChild) {
        e.removeChild(e.firstChild);
    }
}

const refreshTasksTable = () => {
    fetch("/tasks-json")
        .then(response => response.json())
        .then(data => {
            const newTable = document.createElement("table");
            newTable.appendChild(generateTableHeader());
            const tbody = document.createElement("tbody");
            for (let task of data.all_tasks) {
                const tr = document.createElement("tr");
                for (let key of taskKeys) {
                    tr.appendChild(elementWithText("td", task[key]));
                }
                tbody.appendChild(tr);
            }
            newTable.appendChild(tbody);
            const tableContainer = document.getElementById("tasks-table-container");
            removeAllChildren(tableContainer);
            tableContainer.appendChild(newTable);
        })
        .catch(error => {
            console.error("Error when trying to GET new contents for tasks table:", error);
        });
}

const getRemainingProcesses = () => {
    const gameNameInput = document.getElementById('game-name-input');
    if (gameNameInput === null || gameNameInput === undefined) {
        return;
    }

    const gameName = gameNameInput.value;
    if (gameName === null || gameName === undefined || gameName === '') {
        return;
    }

    fetch(`/game-json?game_name=${gameName}`)
        .then(response => response.json())
        .then(data => {
            const gameProcessorsTab = document.getElementById('active-game-processors');

            if (data !== null && data !== undefined && data[gameName] !== null && data[gameName] !== undefined) {
                gameProcessorsTab.innerHTML = `Number of active processes for game: ${gameName} : ${data[gameName]}`;
            } else {
                gameProcessorsTab.innerHTML = 'Error!';
            }
        })
        .catch(error => {
            console.error(`Error when trying to GET number of live processes for game: ${gameName}`, error);
        });
}

document.addEventListener("DOMContentLoaded", _ => {
    refreshTasksTable();

    const refreshButton = document.getElementById("refresh-button");
    refreshButton.addEventListener("click", refreshTasksTable);
});

document.addEventListener("DOMContentLoaded", _ => {
    refreshTasksTable();

    const refreshButton = document.getElementById("search-game-processors");
    refreshButton.addEventListener("click", getRemainingProcesses);
});
