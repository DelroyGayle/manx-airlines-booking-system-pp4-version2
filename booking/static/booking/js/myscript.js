// Hide/Show elements depending on '#theReturn'

function hide_returning_option() {
    $("span:contains('DD/');:nth-of-type(2);").hide();
    $("label:contains('Returning');:nth-of-type(2);").hide();
    $('label[for="id_returning_date"]').hide();
    $("#id_returning_date").hide();
    $('label[for="id_returning_time_0"]').hide();
    $("#id_returning_time").hide();
}

function show_returning_option() {
    $("span:contains('DD/');:nth-of-type(2);").show();
    $("label:contains('Returning');:nth-of-type(2);").show();
    $('label[for="id_returning_date"]').show();
    $("#id_returning_date").show();
    $('label[for="id_returning_time_0"]').show();
    $("#id_returning_time").show();
}

function returnCheck() {
    let theReturn = document.getElementById("id_return_option").value;
    if (theReturn === "N") {
        hide_returning_option();
    } else {
        show_returning_option();
    }
}

function infantsCheck() {
    let infantsValue = Number(document.getElementById("id_infants").value);
    let adultsValue = Number(document.getElementById("id_adults").value);
    // Defensive Code
    if (!Number.isInteger(infantsValue)) {
        infantsValue = 0;
        document.getElementById("id_infants").value = "0";
    }
    if (!Number.isInteger(adultsValue)) {
        adultsValue = 1;
        document.getElementById("id_adults").value = "1";
    }

    // Check that number of infants does NOT exceed the number of infants
    if (infantsValue > adultsValue) {
        openTooManyInfantsModal();
        document.getElementById("id_infants").focus();
        return false // Indicate Test Failure
    }

    return true // Indicate Test Success
}

function checkReturnFlightOption() {
    if ($("#id_returning_date").length) {
        returnCheck();
    }
}

const openTooManyInfantsModal = () => {
    $(".ui.modal.toomanyinfants").modal("show");
}

const openNoAdultsModal = () => {
    $(".ui.modal.no_adults").modal("show");
}


$(document).ready( function() {
    checkReturnFlightOption();
});

// This solution regarding .ready() not trigggering when Back Button pressed was found at
// https://stackoverflow.com/questions/11871253/execute-document-ready-even-if-user-came-to-the-page-by-hitting-the-back-button

$(window).on("pageshow", function() {
    checkReturnFlightOption();
});