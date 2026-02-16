document.addEventListener("DOMContentLoaded", function () {
    const collegeInput = document.getElementById("collegeInput");
    const suggestionsBox = document.getElementById("collegeSuggestions");

    let colleges = [];

    fetch("/static/data/colleges.json")
        .then((response) => response.json())
        .then((data) => {
            colleges = data;
        });

    collegeInput.addEventListener("input", function () {
        const query = this.value.toLowerCase();
        suggestionsBox.innerHTML = "";

        if (!query) return;

        const matches = colleges
            .filter(college => college.toLowerCase().includes(query))
            .slice(0, 10); // show top 10

        matches.forEach(match => {
            const suggestion = document.createElement("div");
            suggestion.className = "suggestion";
            suggestion.textContent = match;
            suggestion.onclick = () => {
                collegeInput.value = match;
                suggestionsBox.innerHTML = "";
            };
            suggestionsBox.appendChild(suggestion);
        });
    });

    document.addEventListener("click", function (e) {
        if (!collegeInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.innerHTML = "";
        }
    });
});
