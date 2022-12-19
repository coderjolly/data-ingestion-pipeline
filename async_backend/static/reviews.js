const elementWithText = (tag, text) => {
    const e = document.createElement(tag);
    e.innerText = text;
    return e;
}

const taskKeys = ['app_id', 'app_name', 'review_id', 'language', 'review', 'timestamp_updated', 'recommended'];

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

const createTableFromData = (data) => {
    const newTable = document.createElement("table");
    newTable.appendChild(generateTableHeader());
    const tbody = document.createElement("tbody");
    for (let task of data['reviews']) {
        const tr = document.createElement("tr");
        for (let key of taskKeys) {
            tr.appendChild(elementWithText("td", task[key]));
        }
        tbody.appendChild(tr);
    }
    newTable.appendChild(tbody);

    return newTable;
}

const getReviewsData = () => {
    const gameNameInput = document.getElementById('game-name-input-for-data');
    if (gameNameInput === null || gameNameInput === undefined) {
        return;
    }

    const gameName = gameNameInput.value;
    if (gameName === null || gameName === undefined || gameName === '') {
        return;
    }

    fetch(`/reviews-data?game_name=${gameName}`)
        .then(response => response.json())
        .then(data => {
            const tableContainer = document.getElementById("game-reviews");
            removeAllChildren(tableContainer);

            if (data === null || data === undefined || typeof data !== 'object') {
                return;
            }

            const newTable = createTableFromData(data);
            tableContainer.appendChild(newTable);
        })
        .catch(error => {
            console.error(`Error when trying to GET reviews data for game: ${gameName}`, error);
        });
}

document.addEventListener("DOMContentLoaded", _ => {
    const refreshButton = document.getElementById("search-game-for-data");
    refreshButton.addEventListener("click", getReviewsData);
});
