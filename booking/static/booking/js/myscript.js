
   // Hide/Show elements depending on 'theReturn'
   function returnCheck() {
    let theReturn = document.getElementById("id_return_option").value;
    if (theReturn === "N") {
        $("#id_returning_date").hide();
        $("#id_returning_time").hide();
    } else {
        $("#id_returning_date").show();
        $("#id_returning_time").show();
    }
}

function checkURL() {
    let currentURL = window.location.href;
    if (currentURL.endsWith("create/")){
        returnCheck();
    }
}
    
function infantsCheck() {
    
    let infantsValue = Number(document.getElementById("id_infants").value);
    let adultsValue = Number(document.getElementById("id_adults").value);
    // Defensive Code
    if (!Number.isInteger(infantsValue)) {
        infantsValue = 0
        document.getElementById("id_infants").value="0"
    }
    if (!Number.isInteger(adultsValue)) {
        adultsValue = 1
        document.getElementById("id_adults").value="1";
    }

    // Check that number of infants does NOT exceed the number of infants
    if (infantsValue > adultsValue)
    {
        openTooManyInfantsModal();
        document.getElementById("id_infants").focus();
        return false // Indicate Test Failure
    }

    return true  // Indicate Test Success
}

const openTooManyInfantsModal = () => {
    $('.ui.modal.toomanyinfants').modal('show');
}

const openNoAdultsModal = () => {
    $('.ui.modal.no_adults').modal('show');
}

$(document).ready(function(){
    // your code
    checkURL()
});