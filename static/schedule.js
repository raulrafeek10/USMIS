const input = document.getElementById("searchInput");

input.addEventListener("keyup", function () {

    let filter = input.value.toLowerCase();

    let table = document.getElementById("scheduleTable");

    let td = table.getElementsByTagName("td");

    for (let i = 0; i < td.length; i++) {

        let txtValue = td[i].textContent || td[i].innerText;

        td[i].classList.remove("highlight");

        if (txtValue.toLowerCase().includes(filter) && filter !== "") {

            td[i].classList.add("highlight");

            td[i].scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
        }
    }

});